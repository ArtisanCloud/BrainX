import {backendClient} from "@/app/api/backend";
import {RequestCreateMediaResource, ResponseCreateMediaResource} from "@/app/api/media-resource";
import {User} from "@/app/api/tenant/user";

export interface Token {
	token_type: string
	expires_in: number
	access_token: string
	refresh_token: string
}

export interface RequestLogin {
	account: string
	password: string
}

export interface ResponseLogin {
	account: string
	token: Token
}

export async function ActionLogin(option: RequestLogin) {
	// 处理上传事件的逻辑
	const endpoint = `/api/auth/login`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseLogin;
}



export interface RequestRegister {
	account: string
	password: string
}

export interface ResponseRegister {
	user: User
}
export async function ActionRegister(option: RequestRegister) {
	// 处理上传事件的逻辑
	const endpoint = `/api/media/resource/create/base64`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseRegister;
}
