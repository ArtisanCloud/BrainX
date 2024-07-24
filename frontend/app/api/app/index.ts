import {unstable_noStore as noStore} from 'next/cache';
import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";


export interface App extends PowerModel {
	tenant_uuid?: string;
	created_user_by?: string;
	updated_user_by?: string;
	app_model_config_uuid?: string;
	workflow_uuid?: string;
	name?: string;
	status?: string;
	type?: string;
	mode?: string;
	description?: string;
	persona?: string;
	avatar_url?: string;
	is_public?: boolean;
}

export interface ResponseFetchAppList {
	data: App[];
	pagination: ResponsePagination;
}


export async function ActionFetchAppList(pg: RequestPagination): Promise<ResponseFetchAppList> {
	noStore();
	try {
		const endpoint = `/api/app/list`;
		const queryString = Object.entries(pg).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchAppList;

	} catch (error) {
		// console.error('Fetch apps Error:', error);
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

	const endpoint = `/api/app/create`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateApp;

}


export type RequestPatchApp = App

export interface ResponsePatchApp extends Response {
	app: App
}

export async function ActionPatchApp(option: RequestPatchApp): Promise<ResponsePatchApp> {

	const endpoint = `/api/app/patch/${option.uuid}`;

	const res = await backendClient.backend_patch(endpoint, option);

	return res as ResponseCreateApp;

}

export interface ResponseDeleteApp {
	result: boolean
}

export async function ActionDeleteApp(appUuid: string): Promise<ResponseDeleteApp> {

	const endpoint = `/api/app/delete/${appUuid}`

	const res = await backendClient.backend_delete(endpoint);

	return res as ResponseDeleteApp;

}
