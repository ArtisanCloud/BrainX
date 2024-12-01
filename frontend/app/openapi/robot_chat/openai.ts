import {backendUrl} from "@/app/config/config";
import {Message} from "@/app/api/robot-chat/conversation";

export const UriWebChatBot = '/api/chat_bot';

export interface RequestSendOpenAIChat{
	conversation_uuid: string,
	app_uuid?: string,
	model: string,
	images?: string[]
	messages: Message[],
}


export interface Usage {
	prompt_tokens?: number;
	completion_tokens?: number;
	total_tokens?: number;
}

export const GetChatBotSSEActionUrl = (
	action: string,
): string => {
	// const channel = 'glm';
	return backendUrl + `${UriWebChatBot}/${action}`;
};
