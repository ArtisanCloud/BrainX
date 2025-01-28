import {
  FetchFrom,
  ModelFeature,
  ModelPropertyKey,
  I18nObject,
} from "@/app/api/model-provider/index";

/**
 * 枚举：ModelType
 * 用于定义模型的类型。
 */
export enum ModelType {
  LLM = "llm",
  EMBEDDING = "embedding",
  TEXT_EMBEDDING = "text-embedding",
  IMAGE_EMBEDDING = "image-embedding",
  RERANK = "rerank",
  SPEECH2TEXT = "speech2text",
  MODERATION = "moderation",
  TTS = "tts",
  TEXT2IMG = "text2img",
  IMG2IMG = "img2img",
  TEXT2VIDEO = "text2video",
}

/**
 * 接口：ProviderModel
 * 定义 provider 的模型信息。
 */
export interface ProviderModel {
  model: string; // 模型名称
  label: I18nObject; // 多语言标题
  model_type: ModelType; // 模型类型
  features?: ModelFeature[]; // 特性列表（可选）
  fetch_from: FetchFrom; // 获取方式
  model_properties: Record<ModelPropertyKey, any>; // 模型属性
  deprecated?: boolean; // 是否弃用，默认 false
}
