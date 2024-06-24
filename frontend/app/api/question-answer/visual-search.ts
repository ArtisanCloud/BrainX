import {backendClient} from "@/app/api/backend";
import {ImageDocument} from "@/app/api/question-answer/index";
import {Response} from "@/app/api";

export interface RequestVisualSearch {
	question_image: string
	llm: string
}

export interface ResponseVisualSearch extends Response {
	image_documents: ImageDocument[]
}

export const ActionVisualSearch = async (
	params: RequestVisualSearch
): Promise<ResponseVisualSearch> => {
	// const endpoint = `/api/system/test/timeout?timeout=3`
	// const res = await backendClient.backend_get(endpoint, params);
	const endpoint = `/api/question_answer/visual_search`;
	const res = await backendClient.backend_post(endpoint, params);

	return res as ResponseVisualSearch;
}