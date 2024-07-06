import {backendUrl} from "@/app/config/config";
import {Message} from "@/app/api/robot-chat/conversation";

export const UriWebChatBot = '/api/chat_bot';

export interface RequestSendChat{
	conversationUUID: string,
	appUUID?: string,
	llm?: string,
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
