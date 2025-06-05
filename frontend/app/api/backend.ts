import {backendUrl, frontendUrl} from "@/app/config/config";
import {notification} from 'antd';
import {Response as APIResponse} from "@/app/api";
import Cookies from "js-cookie";
import {token_key} from "@/app/utils/auth";
import {sleep} from "@/app/lib/base";

interface validateError {
	type: string
	loc: string[]
	msg: string
	input: any
	url: string
}

interface validateError {
	detail: validateError[]
}


class BackendClient {

	private get_header() {
		const token = Cookies.get(token_key)

		const headers: any = {
			"Content-Type": "application/json",
		}
		if (token) {
			headers['Authorization'] = `Bearer ${token}`
		}
		// console.log(token, headers)


		return headers
	}

	public async backend_get(endpoint: string, init?: any) {
		if (init?.params){
		const queryString = Object.entries(init.params).map(([key, value]) => `${key}=${value}`).join('&');
			endpoint = `${endpoint}?${queryString}`
		}
		// console.log(init?.params,endpoint)
		return this.get(backendUrl, endpoint, init)
	}

	public async backend_post(endpoint: string, body?: any) {
		return this.post(backendUrl, endpoint, body)
	}

	public async backend_post_form(endpoint: string, formData: FormData) {
		return this.postForm(backendUrl, endpoint, formData);
	}

	public async backend_patch(endpoint: string, body?: any) {
		return this.patch(backendUrl, endpoint, body)
	}

	public async backend_delete(endpoint: string, body?: any) {
		return this.delete(backendUrl, endpoint, body)
	}


	public async frontend_get(endpoint: string, init?: any) {
		return this.get(frontendUrl, endpoint, init)
	}

	public async frontend_post(endpoint: string, body?: any) {
		return this.post(frontendUrl, endpoint, body)
	}

	public async get(host: string, endpoint: string, init?: any): Promise<any> {
		const url = host + endpoint;
		const headers = init?.headers ? {...this.get_header(), ...init.headers} : this.get_header();
		const newInit = {...init, headers};
		const res = await fetch(url, newInit);

		return this.processResponse(res)
	}

	public async post(host: string, endpoint: string, body?: any): Promise<any> {
		const url = host + endpoint;
		const res = await fetch(url, {
			method: "POST",
			headers: this.get_header(),
			body: JSON.stringify(body),
		});

		return this.processResponse(res)
	}

	public async postForm(host: string, endpoint: string, formData: FormData): Promise<any> {
		const url = host + endpoint;
		const headers = this.get_header();
		delete headers['Content-Type']; // 让浏览器自动设置 multipart/form-data

		const res = await fetch(url, {
			method: "POST",
			headers: headers,
			body: formData,
		});

		return this.processResponse(res);
	}

	public async patch(host: string, endpoint: string, body?: any): Promise<any> {
		const url = host + endpoint;
		const res = await fetch(url, {
			method: "PATCH",
			headers: this.get_header(),
			body: JSON.stringify(body),
		});

		return this.processResponse(res)
	}

	public async delete(host: string, endpoint: string, body?: any): Promise<any> {
		const url = host + endpoint;
		const res = await fetch(url, {
			method: "DELETE",
			headers: this.get_header(),
			body: JSON.stringify(body),
		});

		return this.processResponse(res)
	}

	private async processHttpErrorResponse(res: Response) {
		if (res.status == 422) {
			const errorResponse = await res.json() as validateError;
			const errors = errorResponse.detail;
			errors.map((error) => {
				notification.warning({
					message: error.msg,
					description: `${error.loc.join(": ")} ${JSON.stringify(error.input)}`,
				});
			});
		} else if (res.status == 401) {

			notification.error({
				message: "当前未登录状态",
				description: "需要重新登录",
				duration: 3,
			});
			sleep(2000).then(() => {
				window.location.href = '/user/login'; // 替换为你的登录页面路径
			})
			return;
		}

	}

	private async processStatusErrorResponse(result: APIResponse) {
		notification.error({
			message: result.error,
			description: result.detail,
		});
	}

	private async processResponse(res: Response) {

		if (!res.ok) {
			await this.processHttpErrorResponse(res);
			throw new Error(`HTTP error! status: ${res.status}`);
		}

		// 根据 Content-Type 处理响应
		const contentType = res.headers.get("Content-Type");

		if (contentType && contentType.includes("image/svg+xml")) {
			// 处理 SVG 响应，返回纯文本内容
			const svgContent = await res.text();
			return svgContent;
		} else if (contentType && contentType.includes("application/json")) {
			// 处理 JSON 响应
			const result = await res.json() as APIResponse;
			if (result.error != null && result.error != '') {
				await this.processStatusErrorResponse(result);
				throw new Error(`request error: ${result.error}`);
			}
			return result;
		} else if (contentType && contentType.includes("image/png")) {
			// 处理 PNG 图片，返回二进制 Blob 数据
			const imageBlob = await res.blob();
			const imageUrl = URL.createObjectURL(imageBlob); // 创建图片的 URL
			return imageUrl;
		} else {
			// 其他类型的处理（如图片或文本）
			const textContent = await res.text();
			return textContent;
		}
	}

}


export const backendClient = new BackendClient();
