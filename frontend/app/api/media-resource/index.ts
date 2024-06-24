import {PowerModel} from "@/app/api";
import {backendClient} from "@/app/api/backend";

export const bucket_name = 'bucket.brainx'

export interface MediaResource extends PowerModel {
	filename: string;
	size: number;
	url: string;
	bucketName: string;
	isLocalStored: boolean;
	contentType: string;
	resourceType: string;
	sortIndex: number;
}

export interface RequestCreateMediaResource {
	mediaName: string
	bucketName: string
	base64Data: string
}

export interface ResponseCreateMediaResource {
	media_resource: MediaResource
	isOSS: boolean;
}


export async function ActionCreateMediaResource(option: RequestCreateMediaResource, sortIndex: number) {
	// 处理上传事件的逻辑
	const endpoint = `/api/media/resource/create/base64`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateMediaResource;
}
