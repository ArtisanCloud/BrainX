import {backendClient} from "@/app/api/backend";

export interface RequestRunMultiple30SecondsTasks {
  task_count: number
}

export interface ResponseRunMultiple30SecondsTasks {
  task_ids: string[]
}


export async function ActionRunMultiple30SecondsTasks(option: RequestRunMultiple30SecondsTasks): Promise<ResponseRunMultiple30SecondsTasks> {

  const endpoint = `/api/task/run-multiple-30s-tasks`

  const res = await backendClient.backend_post(endpoint, option);

  return res as ResponseRunMultiple30SecondsTasks;

}


export interface RequestQueryTasksStatus {
  task_uuids: string[]
}

export interface ResponseQueryTasksStatus {
  [taskId: string]: {
    state: string;  // 任务状态
    current?: number; // 当前进度（可选）
    total?: number;   // 总进度（可选）
    result?: any;     // 结果（可选）
  };
}

export async function ActionQueryTasksStatus(option: RequestQueryTasksStatus): Promise<ResponseQueryTasksStatus> {

  const endpoint = `/api/task/status`

  const res = await backendClient.backend_post(endpoint, option);

  return res as ResponseQueryTasksStatus;

}

