import {unstable_noStore as noStore} from 'next/cache';
import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";
import {Dataset} from "@/app/api/knowledge/dataset";
import {DocumentSegment} from "@/app/api/knowledge/document-segment";


export enum DocumentType {
	TEXT = 1,
	IMAGE = 2,
	AUDIO = 3,
	VIDEO = 4,
}

export enum DocumentStatus {
	DRAFT = 1,
	PUBLISHED = 2,
	ARCHIVED = 3,
}

export interface Document extends PowerModel {
	tenant_uuid?: string;
	dataset_uuid?: string;
	created_user_by?: string;
	updated_user_by?: string;
	title?: string;
	status?: DocumentStatus;
	type?: DocumentType;
	document_index?: number;
	batch_index?: number;
	word_count?: number;
	token_count?: number;
	process_start_at?: string;
	process_end_at?: string;
	parse_start_at?: string;
	parse_end_at?: boolean;
	split_start_at?: number;
	split_end_at?: number;
	dataset?: Dataset;
	document_segments?: DocumentSegment[];

}

export interface RequestFetchDocumentList extends RequestPagination{
	dataset_uuid: string
}

export interface ResponseFetchDocumentList {
	data: Document[];
	pagination: ResponsePagination;
}


export async function ActionFetchDocumentList(pg: RequestFetchDocumentList): Promise<ResponseFetchDocumentList> {
	noStore();
	try {
		const endpoint = `/api/rag/dataset/document/list`;
		const queryString = Object.entries(pg).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchDocumentList;

	} catch (error) {
		// console.error('Fetch documents Error:', error);
		throw new Error('Failed to fetch the latest documents.');
	}
}

export type RequestGetDocument = Document

export interface ResponseGetDocument extends Response {
	document: Document
}

export async function ActionGetDocument(option: RequestGetDocument): Promise<ResponseGetDocument> {
	noStore();
	try {
		const endpoint = `/api/rag/document/${option.uuid}`;
		const res = await backendClient.backend_get(`${endpoint}`, {cache: 'no-store'});

		return res as ResponseGetDocument;

	} catch (error) {
		// console.error('Fetch document Error:', error);
		throw new Error('Failed to fetch the latest document.');
	}
}


export interface RequestCreateDocument {
	name: string
	description: string
	avatar_url: string
	import_type: number
}

export interface ResponseCreateDocument extends Response {
	document: Document
}

export async function ActionCreateDocument(option: RequestCreateDocument): Promise<ResponseCreateDocument> {

	const endpoint = `/api/rag/document/create`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateDocument;

}


export type RequestPatchDocument = Document

export interface ResponsePatchDocument extends Response {
	document: Document
}

export async function ActionPatchDocument(option: RequestPatchDocument): Promise<ResponsePatchDocument> {

	const endpoint = `/api/rag/document/patch/${option.uuid}`;

	const res = await backendClient.backend_patch(endpoint, option);

	return res as ResponseCreateDocument;

}

export interface ResponseDeleteDocument {
	result: boolean
}

export async function ActionDeleteDocument(documentUuid: string): Promise<ResponseDeleteDocument> {

	const endpoint = `/api/rag/document/delete/${documentUuid}`

	const res = await backendClient.backend_delete(endpoint);

	return res as ResponseDeleteDocument;

}
