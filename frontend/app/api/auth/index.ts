import {backendClient} from "@/app/api/backend";
import {User} from "@/app/api/tenant/user";
import {Response} from "@/app/api";

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

export interface ResponseLogin extends Response {
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

export interface ResponseRegister extends Response {
	user: User
}
export async function ActionRegister(option: RequestRegister) {
	// 处理上传事件的逻辑
	const endpoint = `/api/auth/register`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseRegister;
}
