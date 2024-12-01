import {backendUrl} from "@/app/config/config";
import {Message} from "@/app/api/robot-chat/conversation";

export const UriOpenAPIChatBot = '/openapi/v1/chat_bot';

export interface RequestSendChat{
	conversationUUID: string,
	appUUID?: string,
	llm?: string,
	images?: string[]
	messages: Message[],
}


export interface Usage {
	prompt_tokens?: number;
	completion_tokens?: number;
	total_tokens?: number;
}


export interface SSEOpenAIChoice {
    index: number;
    delta: {
        role: string;
        content: string;
    };
    logprobs: null;
    finish_reason: string | null;
}

export interface SSEOpenAIMessage {
    id: string;
    object: string;
    created: number;
    model: string;
    system_fingerprint: string;
    choices: SSEOpenAIChoice[];
    usage: null | {
        prompt_tokens?: number;
        completion_tokens?: number;
        total_tokens?: number;
    };
	status?:string;
}

export const GetOpenAPIChatBotSSEActionUrl = (
	action: string,
): string => {
	// const channel = 'glm';
	return backendUrl + `${UriOpenAPIChatBot}/${action}`;
};
