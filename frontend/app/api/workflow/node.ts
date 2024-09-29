import {unstable_noStore as noStore} from "next/dist/server/web/spec-extension/unstable-no-store";
import {backendClient} from "@/app/api/backend";

enum NodeType {
  AGENT = "agent_bot",
  START = "start_input",
  END = "end_result",
  PLUGIN = "plugin",
  LLM = "llm",
  CODE = "code",
  KNOWLEDGE = "knowledge",
  WORKFLOW = "workflow",
  CONDITION = "condition",
  LOOP = "loop",
  INTENT_RECOGNITION = "intent_recognition",
  TEXT_PROCESSING = "text_processing",
  MESSAGE = "message",
  QUESTION = "question",
  VARIABLE = "variable",
  DATABASE = "database"
}

export interface NodeTypeInfo {
  id: string;
  type: string;
  name: string;
  icon: string;
  description: string;
  support_batch: boolean;
}


export interface ResponseFetchNodeList {
  data: NodeTypeInfo[];
}


export async function ActionFetchNodeList(): Promise<ResponseFetchNodeList> {
  noStore();
  try {
    const endpoint = `/api/workflow/node/list`;
    const res = await backendClient.backend_get(`${endpoint}`, {
      headers: {
        'Cache-Control': 'max-age=7200', // 设置缓存时间为 2 小时
      }
    });

    return res as ResponseFetchNodeList;

  } catch (error) {
    // console.error('Fetch nodes Error:', error);
    throw new Error('Failed to fetch the latest nodes.');
  }
}
