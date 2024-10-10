import {backendClient} from "@/app/openapi/backend";
import {backendUrl} from "@/app/config/config";
import {Response} from "@/app/api";

export interface RequestChat {
  template: string
  question: string
  llm: string
  temperature: number
  base64_file: string
  name: string
  message: string
}

export interface ResponseChat {
  document: string
}

export const ActionDemoChatCompletion = async (
  params: RequestChat
): Promise<Response> => {
  const endpoint = `/openapi/v1/demo/hello-world`;
  const res = await backendClient.backend_post(endpoint, params);

  return res as Response;
}

export const GetDemoChatSSEActionUrl = (
  action: string,
): string => {
  return backendUrl + `/openapi/v1/demo/stream`;
};

