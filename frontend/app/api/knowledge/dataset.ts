import {unstable_noStore as noStore} from 'next/cache';
import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";


export enum DatasetImportType {
	LOCAL_DOCUMENT = 1,
	ONLINE_DATA = 2,
	NOTION = 3,
	GOOGLE_DOC = 4,
	LARK = 5,
	CUSTOM = 6,
}

export interface Dataset extends PowerModel {
	tenant_uuid?: string;
	created_user_by?: string;
	updated_user_by?: string;
	name?: string;
	description?: string;
	avatar_url?: string;
	is_published?: boolean;
	import_type?: string;
	driver_type?: string;
	embedding_model?: string;
	embedding_model_provider?: string;

}

export interface ResponseFetchDatasetList {
	data: Dataset[];
	pagination: ResponsePagination;
}


export async function ActionFetchDatasetList(pg: RequestPagination): Promise<ResponseFetchDatasetList> {
	noStore();
	try {
		const endpoint = `/api/rag/dataset/list`;
		const queryString = Object.entries(pg).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchDatasetList;

	} catch (error) {
		console.error('Fetch datasets Error:', error);
		throw new Error('Failed to fetch the latest datasets.');
	}
}


export interface RequestCreateDataset {
	name: string
	description: string
	avatar_url: string
}

export interface ResponseCreateDataset extends Response {
	dataset: Dataset
}

export async function ActionCreateDataset(option: RequestCreateDataset): Promise<ResponseCreateDataset> {

	const endpoint = `/api/rag/dataset/create`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateDataset;

}


export type RequestPatchDataset = Dataset

export interface ResponsePatchDataset extends Response {
	dataset: Dataset
}

export async function ActionPatchDataset(option: RequestPatchDataset): Promise<ResponsePatchDataset> {

	const endpoint = `/api/rag/dataset/patch/${option.uuid}`;

	const res = await backendClient.backend_patch(endpoint, option);

	return res as ResponseCreateDataset;

}

export interface ResponseDeleteDataset {
	result: boolean
}

export async function ActionDeleteDataset(datasetUuid: string): Promise<ResponseDeleteDataset> {

	const endpoint = `/api/rag/dataset/delete/${datasetUuid}`

	const res = await backendClient.backend_delete(endpoint);

	return res as ResponseDeleteDataset;

}
