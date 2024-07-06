import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";
import {unstable_noStore as noStore} from "next/dist/server/web/spec-extension/unstable-no-store";
import {App} from "@/app/api/robot-chat/app";

export interface Message extends PowerModel{
	role: string
	content: string
}

export interface Conversation extends PowerModel{
	currentPrompt: string;
	messages?: Message[];
	items: ConversationItem[];

}

export interface ConversationItem {
	question: string;
	answer: string;
}

export interface ResponseFetchConversationList {
	data: Conversation[];
	pagination: ResponsePagination;
}



export async function ActionFetchConversationList(pg: RequestPagination): Promise<ResponseFetchConversationList> {
	noStore();
	try {
		const endpoint = `/api/chat_bot/conversation/list`;
		const queryString = Object.entries(pg).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchConversationList;

	} catch (error) {
		console.error('Fetch conversations Error:', error);
		throw new Error('Failed to fetch the latest conversations.');
	}
}

export interface RequestCreateConversation {
	name?: string
	app_uuid: string
}

export interface ResponseCreateConversation extends Response {
	conversation: Conversation
}

export async function ActionCreateConversation(option: RequestCreateConversation): Promise<ResponseCreateConversation> {

	const endpoint = `/api/chat_bot/conversation/create`;

	const res = await backendClient.backend_post(endpoint, option);

	return res as ResponseCreateConversation;

}
