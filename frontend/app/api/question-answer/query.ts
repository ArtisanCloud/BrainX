import {backendClient} from "@/app/api/backend";

export interface RequestQAQuery {
	question: string
	llm:string
}

export interface ResponseQAQuery {
	answer: string
}

export const ActionQAQuery = async (
	params: RequestQAQuery
): Promise<ResponseQAQuery> => {
	// const endpoint = `/api/system/test/timeout?timeout=3`
	// const res = await backendClient.backend_get(endpoint, params);
	const endpoint = `/api/question-answer/query`;
	const res = await backendClient.backend_post(endpoint, params);

	return  res as ResponseQAQuery;
}
