from decimal import Decimal
from typing import Mapping, Any

from langchain_ollama import ChatOllama
from pydantic import Field

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider_model import ModelFeature, ModelPropertyKey, FetchFrom
from app.core.brainx.entity.runtime.provider_model import AIModelEntity, ModelType, ParameterRule, DefaultParameterName, ParameterType, PriceConfig
from app.core.brainx.interface.llm import LLM
from app.core.exception.exceptions import ProviderModelCredentialNotProvidedException


class OllamaLLM(LLM):
    model_id: str = Field(default="", description="模型 ID")
    """
    Model class for Ollama large language model.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(self, credentials: Mapping) -> None:
        llm = self.get_provider_model({
            "credentials": credentials,
            "streaming": False,
        })

        try:
            # model_list = llm.list_models()
            # logger.info(f"Ollama model list: {model_list}")
            llm.invoke("ping")
        except Exception as e:
            raise e

    def get_provider_model(self, params: dict = None) -> Any:
        # 从 params 中获取并进行处理
        credentials = dict(params.get("credentials", {})) if params else {}
        if not credentials:
            raise ProviderModelCredentialNotProvidedException()

        temperature = float(params.get("temperature", 0))  # 默认值 0
        streaming = bool(params.get("streaming", False))  # 默认值 False
        # fmt = str(params.get("format", ""))  # 默认值 ""
        # timeout = int(params.get("timeout", 300))  # 默认值 300

        base_url = credentials.get('base_url')

        # 返回 ChatOllama 实例
        return ChatOllama(
            model=self.model_id,
            base_url=base_url,
            keep_alive=-1,
            temperature=temperature,
            streaming=streaming,
            # format=fmt,
            # timeout=timeout,
        )

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity:
        """
        Get customizable model schema.

        :param model: model name
        :param credentials: credentials

        :return: model schema
        """
        extras = {
            "features": [],
        }

        if "vision_support" in credentials and credentials["vision_support"] == "true":
            extras["features"].append(ModelFeature.VISION)
        if "function_call_support" in credentials and credentials["function_call_support"] == "true":
            extras["features"].append(ModelFeature.TOOL_CALL)
            extras["features"].append(ModelFeature.MULTI_TOOL_CALL)

        entity = AIModelEntity(
            model=model,
            label=I18nObject(zh_Hans=model, en_US=model),
            model_type=ModelType.LLM,
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                ModelPropertyKey.MODE: credentials.get("mode"),
                ModelPropertyKey.CONTEXT_SIZE: int(credentials.get("context_size", 4096)),
            },
            parameter_rules=[
                ParameterRule(
                    name=DefaultParameterName.TEMPERATURE.value,
                    use_template=DefaultParameterName.TEMPERATURE.value,
                    label=I18nObject(en_US="Temperature", zh_Hans="温度"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="The temperature of the model. "
                              "Increasing the temperature will make the model answer "
                              "more creatively. (Default: 0.8)",
                        zh_Hans="模型的温度。增加温度将使模型的回答更具创造性。（默认值：0.8）",
                    ),
                    default=0.1,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name=DefaultParameterName.TOP_P.value,
                    use_template=DefaultParameterName.TOP_P.value,
                    label=I18nObject(en_US="Top P", zh_Hans="Top P"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="Works together with top-k. A higher value (e.g., 0.95) will lead to "
                              "more diverse text, while a lower value (e.g., 0.5) will generate more "
                              "focused and conservative text. (Default: 0.9)",
                        zh_Hans="与top-k一起工作。较高的值（例如，0.95）会导致生成更多样化的文本，而较低的值（例如，0.5）会生成更专注和保守的文本。（默认值：0.9）",
                    ),
                    default=0.9,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name="top_k",
                    label=I18nObject(en_US="Top K", zh_Hans="Top K"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Reduces the probability of generating nonsense. "
                              "A higher value (e.g. 100) will give more diverse answers, "
                              "while a lower value (e.g. 10) will be more conservative. (Default: 40)",
                        zh_Hans="减少生成无意义内容的可能性。较高的值（例如100）将提供更多样化的答案，而较低的值（例如10）将更为保守。（默认值：40）",
                    ),
                    min=1,
                    max=100,
                ),
                ParameterRule(
                    name="repeat_penalty",
                    label=I18nObject(en_US="Repeat Penalty"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="Sets how strongly to penalize repetitions. "
                              "A higher value (e.g., 1.5) will penalize repetitions more strongly, "
                              "while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)",
                        zh_Hans="设置对重复内容的惩罚强度。一个较高的值（例如，1.5）会更强地惩罚重复内容，而一个较低的值（例如，0.9）则会相对宽容。（默认值：1.1）",
                    ),
                    min=-2,
                    max=2,
                ),
                ParameterRule(
                    name="num_predict",
                    use_template="max_tokens",
                    label=I18nObject(en_US="Num Predict", zh_Hans="最大令牌数预测"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Maximum number of tokens to predict when generating text. "
                              "(Default: 128, -1 = infinite generation, -2 = fill context)",
                        zh_Hans="生成文本时预测的最大令牌数。（默认值：128，-1 = 无限生成，-2 = 填充上下文）",
                    ),
                    default=(512 if int(credentials.get("max_tokens", 4096)) >= 768 else 128),
                    min=-2,
                    max=int(credentials.get("max_tokens", 4096)),
                ),
                ParameterRule(
                    name="mirostat",
                    label=I18nObject(en_US="Mirostat sampling", zh_Hans="Mirostat 采样"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Enable Mirostat sampling for controlling perplexity. "
                              "(default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)",
                        zh_Hans="启用 Mirostat 采样以控制困惑度。"
                                "（默认值：0，0 = 禁用，1 = Mirostat，2 = Mirostat 2.0）",
                    ),
                    min=0,
                    max=2,
                ),
                ParameterRule(
                    name="mirostat_eta",
                    label=I18nObject(en_US="Mirostat Eta", zh_Hans="学习率"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="Influences how quickly the algorithm responds to feedback from "
                              "the generated text. A lower learning rate will result in slower adjustments, "
                              "while a higher learning rate will make the algorithm more responsive. "
                              "(Default: 0.1)",
                        zh_Hans="影响算法对生成文本反馈响应的速度。较低的学习率会导致调整速度变慢，而较高的学习率会使得算法更加灵敏。（默认值：0.1）",
                    ),
                    precision=1,
                ),
                ParameterRule(
                    name="mirostat_tau",
                    label=I18nObject(en_US="Mirostat Tau", zh_Hans="文本连贯度"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="Controls the balance between coherence and diversity of the output. "
                              "A lower value will result in more focused and coherent text. (Default: 5.0)",
                        zh_Hans="控制输出的连贯性和多样性之间的平衡。较低的值会导致更专注和连贯的文本。（默认值：5.0）",
                    ),
                    precision=1,
                ),
                ParameterRule(
                    name="num_ctx",
                    label=I18nObject(en_US="Size of context window", zh_Hans="上下文窗口大小"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Sets the size of the context window used to generate the next token. (Default: 2048)",
                        zh_Hans="设置用于生成下一个标记的上下文窗口大小。（默认值：2048）",
                    ),
                    default=2048,
                    min=1,
                ),
                ParameterRule(
                    name="num_gpu",
                    label=I18nObject(en_US="GPU Layers", zh_Hans="GPU 层数"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="The number of layers to offload to the GPU(s). "
                              "On macOS it defaults to 1 to enable metal support, 0 to disable."
                              "As long as a model fits into one gpu it stays in one. "
                              "It does not set the number of GPU(s). ",
                        zh_Hans="加载到 GPU 的层数。在 macOS 上，默认为 1 以启用 Metal 支持，设置为 0 则禁用。"
                                "只要模型适合一个 GPU，它就保留在其中。它不设置 GPU 的数量。",
                    ),
                    min=-1,
                    default=1,
                ),
                ParameterRule(
                    name="num_thread",
                    label=I18nObject(en_US="Num Thread", zh_Hans="线程数"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Sets the number of threads to use during computation. "
                              "By default, Ollama will detect this for optimal performance. "
                              "It is recommended to set this value to the number of physical CPU cores "
                              "your system has (as opposed to the logical number of cores).",
                        zh_Hans="设置计算过程中使用的线程数。默认情况下，Ollama会检测以获得最佳性能。建议将此值设置为系统拥有的物理CPU核心数（而不是逻辑核心数）。",
                    ),
                    min=1,
                ),
                ParameterRule(
                    name="repeat_last_n",
                    label=I18nObject(en_US="Repeat last N", zh_Hans="回溯内容"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Sets how far back for the model to look back to prevent repetition. "
                              "(Default: 64, 0 = disabled, -1 = num_ctx)",
                        zh_Hans="设置模型回溯多远的内容以防止重复。（默认值：64，0 = 禁用，-1 = num_ctx）",
                    ),
                    min=-1,
                ),
                ParameterRule(
                    name="tfs_z",
                    label=I18nObject(en_US="TFS Z", zh_Hans="减少标记影响"),
                    type=ParameterType.FLOAT,
                    help=I18nObject(
                        en_US="Tail free sampling is used to reduce the impact of less probable tokens "
                              "from the output. A higher value (e.g., 2.0) will reduce the impact more, "
                              "while a value of 1.0 disables this setting. (default: 1)",
                        zh_Hans="用于减少输出中不太可能的标记的影响。较高的值（例如，2.0）会更多地减少这种影响，而1.0的值则会禁用此设置。（默认值：1）",
                    ),
                    precision=1,
                ),
                ParameterRule(
                    name="seed",
                    label=I18nObject(en_US="Seed", zh_Hans="随机数种子"),
                    type=ParameterType.INT,
                    help=I18nObject(
                        en_US="Sets the random number seed to use for generation. Setting this to "
                              "a specific number will make the model generate the same text for "
                              "the same prompt. (Default: 0)",
                        zh_Hans="设置用于生成的随机数种子。将此设置为特定数字将使模型对相同的提示生成相同的文本。（默认值：0）",
                    ),
                ),
                ParameterRule(
                    name="keep_alive",
                    label=I18nObject(en_US="Keep Alive", zh_Hans="模型存活时间"),
                    type=ParameterType.STRING,
                    help=I18nObject(
                        en_US="Sets how long the model is kept in memory after generating a response. "
                              "This must be a duration string with a unit (e.g., '10m' for 10 minutes or '24h' for 24 hours)."
                              " A negative number keeps the model loaded indefinitely, and '0' unloads the model"
                              " immediately after generating a response."
                              " Valid time units are 's','m','h'. (Default: 5m)",
                        zh_Hans="设置模型在生成响应后在内存中保留的时间。"
                                "这必须是一个带有单位的持续时间字符串（例如，'10m' 表示10分钟，'24h' 表示24小时）。"
                                "负数表示无限期地保留模型，'0'表示在生成响应后立即卸载模型。"
                                "有效的时间单位有 's'（秒）、'm'（分钟）、'h'（小时）。（默认值：5m）",
                    ),
                ),
                ParameterRule(
                    name="format",
                    label=I18nObject(en_US="Format", zh_Hans="返回格式"),
                    type=ParameterType.TEXT,
                    default="json",
                    help=I18nObject(
                        en_US="the format to return a response in. Format can be `json` or a JSON schema.",
                        zh_Hans="返回响应的格式。目前接受的值是字符串`json`或JSON schema.",
                    ),
                ),
            ],
            pricing=PriceConfig(
                input=Decimal(credentials.get("input_price", 0)),
                output=Decimal(credentials.get("output_price", 0)),
                unit=Decimal(credentials.get("unit", 0)),
                currency=credentials.get("currency", "USD"),
            ),
            **extras,
        )

        return entity
