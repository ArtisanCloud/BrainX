import {PowerModel} from "@/app/api";
import {backendClient} from "@/app/api/backend";

export const bucket_name = 'bucket.brainx'

export interface MediaResource extends PowerModel {
	bucket_name: string;
	filename: string;
	size: number;
	is_local_stored: boolean;
	url: string;
	content_type: string;
	resource_type: string;
	sort_index: number;
}

export interface RequestCreateMediaResource {
	mediaName: string
	bucketName: string
	base64Data: string
	sortIndex: number
}

export interface ResponseCreateMediaResource {
	media_resource: MediaResource
	isOSS: boolean;
}


export async function ActionCreateMediaResource(option: RequestCreateMediaResource) {
	// 处理上传事件的逻辑
	const endpoint = `/api/media/resource/create/base64`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateMediaResource;
}
