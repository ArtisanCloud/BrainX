// 定义帮助信息接口
import {
  FormOption,
  FormShowOnObject,
  FormType,
  MultilingualField,
} from "@/app/api/model-provider/index";
import { ModelType, ProviderModel } from "@/app/api/model-provider/model";
import { backendClient } from "@/app/api/backend";

import { unstable_noStore as noStore } from "next/dist/server/web/spec-extension/unstable-no-store";
import { backendUrl } from "@/app/config/config";

export interface Help {
  // 帮助标题，支持多语言
  title: MultilingualField;
  // 帮助链接，必须是有效的 URL
  url: MultilingualField;
}

// 配置方法枚举
export enum ConfigurateMethod {
  PREDEFINED_MODEL = "predefined", // 预定义模型
  CUSTOMIZED_MODEL = "customized", // 自定义模型
}

// 凭证表单字段接口
export interface CredentialForm {
  // 字段变量名称
  variable: string;
  // 字段标签，支持多语言
  title: MultilingualField;
  // 字段类型，使用 FormType 枚举
  type: FormType;
  // 是否必填，默认为 true
  required?: boolean;
  // 默认值，可选
  default?: string;
  // 字段选项，用于选择类型字段
  options?: FormOption[];
  // 占位符，支持多语言
  placeholder?: MultilingualField;
  // 字段最大长度
  max_length?: number;
  // 字段展示条件
  show_on?: FormShowOnObject[];
}

// 提供者凭证接口
export interface ProviderCredential {
  // 凭证表单字段列表
  credential_form_schemas: CredentialForm[];
}

// 模型字段接口
export interface FieldModel {
  // 字段标题，支持多语言
  title: MultilingualField;
  // 占位符，支持多语言
  placeholder?: MultilingualField;
}

// 模型凭证接口
export interface ModelCredential {
  // 模型字段
  model: FieldModel;
  // 凭证表单字段列表
  credentialForms: CredentialForm[];
}

// 提供者接口
export interface Provider {
  // 提供者名称
  provider: string;
  // 提供者的标题，支持多语言
  title: MultilingualField;
  // 提供者的描述，支持多语言
  description?: MultilingualField;
  // 小图标路径，支持多语言
  iconSmall?: MultilingualField;
  // 大图标路径，支持多语言
  iconLarge?: MultilingualField;
  // 背景颜色（HEX 格式）
  background: string;
  // 帮助信息
  help: Help;
  // 支持的模型类型列表
  supported_model_types: ModelType[];
  // 支持的配置方法列表
  configurate_methods: ConfigurateMethod[];
  // 可用的模型列表，默认为空
  models?: ProviderModel[];
  // 提供者凭证模式，可选
  provider_credential_schema?: ProviderCredential;
  // 模型凭证模式，可选
  models_credential_schema?: ModelCredential;
  // 配置选项（TypeScript 中用于动态字段）
  [key: string]: any;
}

export interface ResponseFetchProviderList {
  data: Record<string, Provider>; // 'data' 是一个键值对对象，键是字符串，值是 Provider 类型
}

export async function ActionFetchProviderList(): Promise<ResponseFetchProviderList> {
  noStore();
  try {
    const endpoint = `/api/model-provider/list`;
    const res = await backendClient.backend_get(endpoint, {
      cache: "no-store",
    });

    return res as ResponseFetchProviderList;
  } catch (error) {
    // console.error('Fetch apps Error:', error);
    throw new Error("Failed to fetch the latest apps.");
  }
}

export async function ActionGetProviderIcon(
  providerName: string
): Promise<any> {
  noStore();
  try {
    const endpoint = `/api/model-provider/icon/${providerName}/icon_large/zh_CN`;
    const resource = await backendClient.backend_get(endpoint, {});
    // 返回直接的 SVG or PNG 内容
    return resource;
  } catch (error) {
    console.error("Fetch apps Error:", error);
    // throw new Error(`Failed to fetch the provider icon : ${error}`);
  }
}
