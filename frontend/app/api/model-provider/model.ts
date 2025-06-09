import {
  FetchFrom,
  ModelFeature,
  ModelPropertyKey,
  I18nObject, ModelTypeEnum,
} from "@/app/api/model-provider/index";
import {backendClient} from "@/app/api/backend";
import {CustomConfigurationStatusEnum, ModelStatusEnum} from "@/app/api/model-provider/provider";


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

export interface ResponseGetProviderModels {
  data: ProviderModel[];
}

export async function ActionGetProviderModels(option: RequestGetProviderModels): Promise<ResponseGetProviderModels> {
  try {
    const endpoint = `/api/model-provider/provider-model/list`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseGetProviderModels;
  } catch (error) {
    throw new Error(`Failed to fetch the provider credentials : ${error}`);
  }
}

export interface RequestChangeModelStatus {
  model_type: string;
  provider: string;
  model: string;
  status: boolean;
}

export interface ResponseChangeModelStatus {
  result: boolean;
}

export async function ActionChangeModelStatus(option: RequestChangeModelStatus): Promise<ResponseChangeModelStatus> {
  try {
    const endpoint = `/api/model-provider/provider-model/status`;
    const res = await backendClient.backend_patch(endpoint, option);
    return res as ResponseChangeModelStatus;
  } catch (error) {
    throw new Error(`Failed to change the provider model status : ${error}`);
  }
}


export interface ModelLoadBalanceConfig {
  enable: boolean;
  configs?: Record<string, any>;
}

export interface RequestSaveProviderModelSetting {
  model_type: string;
  provider: string;
  model: string;
  credentials: Record<string, any>;
  load_balancing: ModelLoadBalanceConfig
}

export interface ResponseSaveProviderModelSetting {
  result: boolean;
}


export async function ActionSaveProviderModelSetting(option: RequestSaveProviderModelSetting): Promise<ResponseSaveProviderModelSetting> {
  try {
    const endpoint = `/api/model-provider/provider-model/save`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseSaveProviderModelSetting;
  } catch (error) {
    throw new Error(`Failed to save the provider credentials : ${error}`);
  }
}

export interface RequestDeleteModel {
  provider: string
  model: string
  model_type: string
}

export interface ResponseDeleteModel {
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

export interface ResponseGetModelCredentials {
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


export interface ProviderModelWithStatusEntity extends ProviderModel {
  status: ModelStatusEnum
  load_balancing_enabled: boolean
}

export interface ProviderWithModels {
  tenant_uuid: string
  provider: string
  label: I18nObject
  icon_small?: I18nObject
  icon_large?: I18nObject
  status: CustomConfigurationStatusEnum
  models: ProviderModelWithStatusEntity[]

}

export interface ResponseGetModelsByType {
  data: ProviderWithModels[];
}


export async function fetchModelsByType(modelType: string) {
  try {
    const endpoint = `/api/model-provider/provider-model/model-types/${modelType}`;
    const res = await backendClient.backend_get(endpoint);
    return res as ResponseGetModelsByType;
  } catch (error) {
    throw new Error(`Failed to fetch the models : ${error}`);
  }
}


export interface ParameterRule {

  name: string
  use_template?: string
  label?: I18nObject
  type?: string
  help?: I18nObject
  required?: boolean
  default?: any
  min?: number
  max?: number
  precision?: number
  options: string[]
}

export interface PriceConfig {
  input: number
  output?: number
  unit: number
  currency: string
}

export interface AIModelEntity extends ProviderModel {

  parameter_rules: ParameterRule[]
  pricing?: [PriceConfig]
}


export interface SimpleProviderEntity {
  provider: string
  label?: I18nObject
  icon_small?: I18nObject
  icon_large?: I18nObject
  supported_model_types: ModelTypeEnum[]
  models: AIModelEntity[]
}

export interface SimpleProviderEntityResponse extends SimpleProviderEntity {
  tenant_uuid: string
}

export interface DefaultModelResponse {

  model: string
  model_type: ModelTypeEnum
  provider: SimpleProviderEntityResponse
}

export interface ResponseGetDefaultModel {
  data: DefaultModelResponse;
}


export async function fetchDefaultModels(modelType: string) {
  try {
    const endpoint = `/api/model-provider/provider-model/default-model/${modelType}`;
    const res = await backendClient.backend_get(endpoint);
    return res as ResponseGetDefaultModel;
  } catch (error) {
    throw new Error(`Failed to fetch the default model: ${error}`);
  }
}

export interface UpdateDefaultModel {

  model_type: string
  provider?: string
  model?: string

}

export interface RequestSaveDefaultModels {
  model_settings: UpdateDefaultModel[]
}

export interface ResponseSaveDefaultModels {
  result: boolean;
}


export async function saveDefaultModels(option: RequestSaveDefaultModels) {
  try {
    const endpoint = `/api/model-provider/provider-model/default-model`;
    const res = await backendClient.backend_post(endpoint, option);
    return res as ResponseSaveDefaultModels;
  } catch (error) {
    throw new Error(`Failed to fetch the default model: ${error}`);
  }
}
