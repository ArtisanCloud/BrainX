import {backendUrl} from "@/app/config/config";

export const UriWebChatBot = '/api/chat_bot';




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
