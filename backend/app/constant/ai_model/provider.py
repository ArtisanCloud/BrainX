from enum import Enum


class ProviderID(Enum):
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    BAICHUAN = "baichuan"
    BEDROCK = "bedrock"
    CHATGLM = "chatglm"
    COHERE = "cohere"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    HUGGINGFACE_HUB = "huggingface_hub"
    JINA = "jina"
    LOCALAI = "localai"
    MINIMAX = "minimax"
    MISTRALAI = "mistralai"
    MOONSHOT = "moonshot"
    NVIDIA = "nvidia"
    NVIDIA_NIM = "nvidia_nim"
    OLLAMA = "ollama"
    OPENAI = "openai"
    OPENAI_API_COMPATIBLE = "openai_api_compatible"
    OPENLLM = "openllm"
    OPENROUTER = "openrouter"
    PERFXCLOUD = "perfxcloud"
    REPLICATE = "replicate"
    SILICONFLOW = "siliconflow"
    SPARK = "spark"
    TENCENT = "tencent"
    TOGETHERAI = "togetherai"
    TONGYI = "tongyi"
    TRITON_INFERENCE_SERVER = "triton_inference_server"
    UPSTAGE = "upstage"
    VOLCENGINE_MAAS = "volcengine_maas"
    WENXIN = "wenxin"
    XINFERENCE = "xinference"
    YI = "yi"
    ZHIPUAI = "zhipuai"
    ZHINAO = "zhinao"


class ModelID(Enum):
    # OpenAI
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

    # 文心一言
    ERNIE_BOT = "ernie-bot"
    ERNIE_BOT_TURBO = "ernie-bot-turbo"
    ERNIE_BOT_4 = "ernie-bot-4"

    # Anthropic
    CLAUDE_INSTANT_1 = "claude-instant-1"
    CLAUDE_2 = "claude-2"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    CLAUDE_3_HAIKU = "claude-3-haiku"

    # MistralAI
    MISTRAL_7B = "mistral-7b"
    MISTRAL_7B_INSTRUCT = "mistral-7b-instruct"
    MIXTRAL_8X7B = "mixtral-8x7b"
    MIXTRAL_8X7B_INSTRUCT = "mixtral-8x7b-instruct"

    # Moonshot
    MOONSHOT_V1 = "moonshot-v1"
    MOONSHOT_V1_128K = "moonshot-v1-128k"

    # DeepSeek
    DEEPSEEK_CHAT = "deepseek-chat"
    DEEPSEEK_CODER = "deepseek-coder"

    # ZhipuAI
    CHATGLM_6B = "chatglm-6b"
    CHATGLM_6B_INT4 = "chatglm-6b-int4"
    CHATGLM2_6B = "chatglm2-6b"
    CHATGLM3_6B = "chatglm3-6b"

    # 百川 Baichuan
    BAICHUAN_7B = "baichuan-7b"
    BAICHUAN_13B = "baichuan-13b"
    BAICHUAN2_7B_CHAT = "baichuan2-7b-chat"
    BAICHUAN2_13B_CHAT = "baichuan2-13b-chat"

    # MiniMax
    MINIMAX_ABAB5_3 = "abab5.3"

    # Yi
    YI_6B_CHAT = "yi-6b-chat"
    YI_34B_CHAT = "yi-34b-chat"

    # Tongyi
    TONGYI_QIANWEN = "qwen-turbo"
    TONGYI_QIANWEN_PLUS = "qwen-plus"

    # 腾讯 Tencent
    TENCENT_HYUN = "hunyuan-chat"

    # 火山引擎 Volcengine
    VOLCENGINE_SKYCHAT = "skychat"

    # Replicate
    LLAMA_2_13B = "llama-2-13b"
    LLAMA_2_70B = "llama-2-70b"

    # Groq
    OLLAMA_DEEPSEEK_R1_1_5B = "deepseek-r1:1.5b"
    OLLAMA_DEEPSEEK_R1_7B = "deepseek-r1:7b"
    OLLAMA_DEEPSEEK_R1_8B = "deepseek-r1:8b"
    OLLAMA_DEEPSEEK_R1_14B = "deepseek-r1:14b"
    OLLAMA_DEEPSEEK_R1_32B = "deepseek-r1:32b"
    OLLAMA_DEEPSEEK_R1_70B = "deepseek-r1:70b"
    OLLAMA_13B_ALPACA_16K = "13B-alpaca-16k:latest"
    OLLAMA_GEMMA_2B = "gemma:2b"
    OLLAMA_GEMMA_7B = "gemma:7b"
    OLLAMA_LLAMA3_2 = "llama3.2"
    OLLAMA_LLAMA3_2_VISION = "llama3.2-vision"
    OLLAMA_LLAMA3_3 = "llama3.3"
    OLLAMA_QWEN_2_5 = "qwen2.5"
    OLLAMA_QWQ_32b = "qwq:32b"
    OLLAMA_QWEN_2_5_72b = "qwen2.5:72b"
    OLLAMA_QWEN_CODER_2_5 = "qwen2.5-coder"
    OLLAMA_DEEP_SEEK_R1_70 = "deepseek-r1:70b"

    # Cohere
    COMMAND_R = "command-r"
    COMMAND_R_PLUS = "command-r-plus"

    # LLAMA_CPP
    LLAMA_CPP_DEEPSEEK_R1_DISTILL_QWEN_1_5B_Q4_K_M = "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"
    LLAMA_CPP_DEEPSEEK_R1_DISTILL_QWEN_70B_Q4_K_M = "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf"
    LLAMA_CPP_DEEPSEEK_R1_DISTILL_QWEN_70B_Q3_K_M = "DeepSeek-R1-Distill-Llama-70B-Q3_K_M.gguf"
