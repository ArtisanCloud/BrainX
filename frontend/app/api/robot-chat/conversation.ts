import {backendClient} from "@/app/api/backend";
import {PowerModel, RequestPagination, Response, ResponsePagination} from "@/app/api";
import {unstable_noStore as noStore} from "next/dist/server/web/spec-extension/unstable-no-store";

export interface Message extends PowerModel {
	role?: string
	content: string
	type: string
}

export interface Conversation extends PowerModel {
	user_uuid?: string;
	app_uuid?: string;
	app_model_config_uuid?: string;
	name?: string;
	status?: string;
	context?: string;
	currentPrompt: string;
	messages?: Message[];
	items: ConversationItem[];

}

export interface ConversationItem {
	question: string;
	answer: string;
}

export interface RequestFetchConversationList extends RequestPagination {
	app_uuid: string;
}

export interface ResponseFetchConversationList {
	data: Conversation[];
	pagination: ResponsePagination;
}


export async function ActionFetchConversationList(data: RequestFetchConversationList): Promise<ResponseFetchConversationList> {
	noStore();
	try {
		const endpoint = `/api/chat_bot/conversation/list`;
		const queryString = Object.entries(data).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchConversationList;

	} catch (error) {
		// console.error('Fetch conversations Error:', error);
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


export interface RequestFetchCachedMessageList extends RequestPagination {
	conversation_uuid: string;

}

export interface ResponseFetchCachedMessageList {
	data: Message[];
	pagination: ResponsePagination;
}

export async function ActionFetchCachedMessageList(data: RequestFetchCachedMessageList): Promise<ResponseFetchCachedMessageList> {
	noStore();
	try {
		const endpoint = `/api/chat_bot/conversation/message/list/cached`;
		const queryString = Object.entries(data).map(([key, value]) => `${key}=${value}`).join('&');
		const res = await backendClient.backend_get(`${endpoint}?${queryString}`, {cache: 'no-store'});

		return res as ResponseFetchCachedMessageList;

	} catch (error) {
		// console.error('Fetch cached messages Error:', error);
		throw new Error('Failed to fetch the cached messages.');
	}
}
