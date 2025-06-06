import {
  FetchFrom,
  ModelFeature,
  ModelPropertyKey,
  I18nObject, ModelTypeEnum,
} from "@/app/api/model-provider/index";
import {backendClient} from "@/app/api/backend";



/**
 * 接口：ProviderModel
 * 定义 provider 的模型信息。
 */
export interface ProviderModel {
  model: string; // 模型名称
  label: I18nObject; // 多语言标题
  model_type: ModelTypeEnum; // 模型类型
  features?: ModelFeature[]; // 特性列表（可选）
  fetch_from: FetchFrom; // 获取方式
  model_properties: Record<ModelPropertyKey, any>; // 模型属性
  deprecated?: boolean; // 是否弃用，默认 false
  status: string;
}

export interface RequestGetProviderModels {
  provider_id: string;
}
export interface ResponseGetProviderModels{
  data: ProviderModel[];
}

export async function ActionGetProviderModels(option: RequestGetProviderModels): Promise<ResponseGetProviderModels> {
  try {
    const endpoint = `/api/model-provider/provider-model/list`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseGetProviderModels;
  }catch (error) {
    throw new Error(`Failed to fetch the provider credentials : ${error}`);
  }
}

export interface RequestChangeModelStatus {
  model_type: string;
  provider: string;
  model: string;
  status: boolean;
}

export interface ResponseChangeModelStatus{
  result: boolean;
}

export async function ActionChangeModelStatus(option: RequestChangeModelStatus): Promise<ResponseChangeModelStatus> {
  try {
    const endpoint = `/api/model-provider/provider-model/status`;
    const res = await backendClient.backend_patch(endpoint, option);
    return res as ResponseChangeModelStatus;
  }catch (error) {
    throw new Error(`Failed to change the provider model status : ${error}`);
  }
}


export interface ModelLoadBalanceConfig{
  enable: boolean;
  configs?: Record<string, any>;
}

export interface RequestSaveProviderModelSetting {
  model_type: string;
  provider: string;
  model: string;
  credentials: Record<string, any>;
  load_balancing:ModelLoadBalanceConfig
}
export interface ResponseSaveProviderModelSetting{
  result: boolean;
}


export async function ActionSaveProviderModelSetting(option: RequestSaveProviderModelSetting): Promise<ResponseSaveProviderModelSetting> {
  try {
    const endpoint = `/api/model-provider/provider-model/save`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseSaveProviderModelSetting;
  }catch (error) {
    throw new Error(`Failed to save the provider credentials : ${error}`);
  }
}

export interface RequestDeleteModel {
  provider: string
  model: string
  model_type: string
}
export interface ResponseDeleteModel{
  result: boolean;
}

export async function ActionDeleteModel(option: RequestDeleteModel): Promise<ResponseDeleteModel> {
  const endpoint = `/api/model-provider/provider-model/delete`
  const res = await backendClient.backend_delete(endpoint, option);
  return res as ResponseDeleteModel;
}


export interface RequestGetModelCredentials {
  provider: string;
  model_type: string;
  model: string;
}
export interface ResponseGetModelCredentials{
  data: object
}

export async function ActionGetModelCredentials(option: RequestGetModelCredentials): Promise<ResponseGetModelCredentials> {
  try {
    const endpoint = `/api/model-provider/provider-model/get_model_credentials`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseGetModelCredentials;
  } catch (error) {
    throw new Error(`Failed to fetch the provider credentials : ${error}`);
  }
}
