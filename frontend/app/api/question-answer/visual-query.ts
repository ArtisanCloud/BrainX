import {backendClient} from "@/app/api/backend";
import {ImageDocument} from "@/app/api/question-answer/index";
import {Response} from "@/app/api";

export interface RequestVisualQuery {
	question: string
	question_image: string
	llm: string
}

export interface ResponseVisualQuery extends Response {
	answer: string
}

export const ActionVisualQuery = async (
	params: RequestVisualQuery
): Promise<ResponseVisualQuery> => {
	const endpoint = `/api/question-answer/visual-query`;
	const res = await backendClient.backend_post(endpoint, params);

	return res as ResponseVisualQuery;
}
