/**
 * 多语言字段接口
 * 用于支持多语言字段，包括中文（可选）和英文字段。
 */
export interface MultilingualField {
  zh_CN?: string; // 中文字段，可选
  en_US: string; // 英文字段，必填
}

/**
 * 枚举：ModelFeature
 * 用于定义 LLM 特性的枚举类型。
 */
export enum ModelFeature {
  TOOL_CALL = "tool-call",
  MULTI_TOOL_CALL = "multi-tool-call",
  AGENT_THOUGHT = "agent-thought",
  VISION = "vision",
  STREAM_TOOL_CALL = "stream-tool-call",
}

/**
 * 枚举：FetchFrom
 * 用于定义模型的获取方式。
 */
export enum FetchFrom {
  PREDEFINED = "predefined",
  CUSTOMIZED = "customized",
}

/**
 * 枚举：ModelPropertyKey
 * 用于定义模型属性的键。
 */
export enum ModelPropertyKey {
  MODE = "mode",
  CONTEXT_SIZE = "context_size",
  MAX_CHUNKS = "max_chunks",
  FILE_UPLOAD_LIMIT = "file_upload_limit",
  SUPPORTED_FILE_EXTENSIONS = "supported_file_extensions",
  MAX_CHARACTERS_PER_CHUNK = "max_characters_per_chunk",
  DEFAULT_VOICE = "default_voice",
  VOICES = "voices",
  WORD_LIMIT = "word_limit",
  AUDIO_TYPE = "audio_type",
  MAX_WORKERS = "max_workers",
}

/**
 * 表单显示条件接口
 * 定义字段何时显示。
 */
export interface FormShowOnObject {
  variable: string; // 变量名称
  value: string; // 当变量的值匹配时显示该字段
}

/**
 * 表单选项接口
 * 定义表单选项，包括多语言标题、值和显示条件。
 */
export interface FormOption {
  title: MultilingualField; // 选项标题，多语言支持
  value: string; // 选项值
  show_on?: FormShowOnObject[]; // 选项显示条件，可选
}

/**
 * 表单字段类型枚举
 * 定义不同的表单字段类型。
 */
export enum FormType {
  INPUT_TEXT = "text-input", // 文本输入
  INPUT_SECRET = "secret-input", // 密码输入
  SELECT = "select", // 选择列表
  RADIO = "radio", // 单选按钮
  SWITCH = "switch", // 开关
}
