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


export const ActionVisualQueryByFile = async (
    params: RequestVisualQuery,
    file: File
): Promise<ResponseVisualQuery> => {
    const formData = new FormData();
    
    // 添加文件
    formData.append('file', file);
    
    // 添加其他参数
    formData.append('question', params.question);
    formData.append('llm', params.llm);
    
    const endpoint = `/api/question-answer/visual-query-by-file`;
    const res = await backendClient.backend_post_form(endpoint, formData);

    return res as ResponseVisualQuery;
}