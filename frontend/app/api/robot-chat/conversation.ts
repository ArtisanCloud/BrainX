import {backendClient} from "@/app/api/backend";
import {RequestCreateMediaResource, ResponseCreateMediaResource} from "@/app/api/media-resource";

export interface Conversation {
	currentPrompt: string;
	items: ConversationItem[];

}

export interface ConversationItem {
	question: string;
	answer: string;
}

export async function ActionGet(option: RequestCreateMediaResource, sortIndex: number) {
	// 处理上传事件的逻辑
	const endpoint = `/api/media/resource/create/base64`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateMediaResource;
}
