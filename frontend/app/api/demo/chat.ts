import {backendClient} from "@/app/api/backend";
import {backendUrl, openApiKey} from "@/app/config/config";
import {Response}  from "@/app/api";
export interface RequestChat {
	template: string
	question: string
	llm: string
	temperature: number
	base64_file: string
}

export interface ResponseChat {
	document: string
}

export const ActionDemoChatCompletion = async (
	params: RequestChat
): Promise<Response> => {
	console.log(openApiKey)
	const endpoint = `/openapi/demo/hello-world` + "?access_key=" + openApiKey;
	const res = await backendClient.backend_post(endpoint, params);

	return res as Response;
}

export const GetDemoChatSSEActionUrl = (
	action: string,
): string => {
	return backendUrl + `/openapi/demo/stream` + "?access_key=" + openApiKey;
};

