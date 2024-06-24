import {unstable_noStore as noStore} from 'next/cache';
import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";

export const pageSize = 10
export const maxPageSize = 999

export interface App extends PowerModel {
	user_id?: number;
	parent_id?: number;
	llm_uuid?: string;
	name?: string;
	description?: string;
	persona_prompt?: string;
	status?: number;
	avatar_url?: string;
}

export interface ResponseFetchAppList {
	data: App[];
	pagination: ResponsePagination;
}


export async function ActionFetchAppList(pg: RequestPagination): Promise<ResponseFetchAppList> {
	noStore();
	try {
		const endpoint = `/api/chat_bot/app/list`;
		const queryString = Object.entries(pg).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchAppList;

	} catch (error) {
		console.error('Fetch apps Error:', error);
		throw new Error('Failed to fetch the latest apps.');
	}
}


export interface RequestCreateApp {
	name: string
	description: string
	avatar_url: string
}

export interface ResponseCreateApp extends Response {
	app: App
}

export async function ActionCreateApp(option: RequestCreateApp): Promise<ResponseCreateApp> {

	const endpoint = `/api/chat_bot/app/create`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateApp;

}


export type RequestPatchApp = App

export interface ResponsePatchApp extends Response {
	app: App
}

export async function ActionPatchApp(option: RequestPatchApp): Promise<ResponsePatchApp> {

	const endpoint = `/api/chat_bot/app/patch/${option.uuid}`;

	const res = await backendClient.backend_patch(endpoint, option);

	return res as ResponseCreateApp;

}

export interface ResponseDeleteApp {
	result: boolean
}

export async function ActionDeleteApp(appUuid: string): Promise<ResponseDeleteApp> {

	const endpoint = `/api/chat_bot/app/delete/${appUuid}`

	const res = await backendClient.backend_delete(endpoint);

	return res as ResponseDeleteApp;

}
