import os
from abc import abstractmethod
from collections.abc import Mapping
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.runtime.defaults import PARAMETER_RULE_TEMPLATE
from app.core.brainx.entity.runtime.provider_model import ModelType, DefaultParameterName, AIModelEntity, FetchFrom
from app.core.libs.yaml import load_yaml_file
from app.utils.position_helper import get_position_map, sort_by_position_map


class AIModel(BaseModel):
    """
    Base class for all models.
    """
    tenant_uuid: str
    model_id: str
    model_type: ModelType
    provider_name: str
    # provider_entity: ProviderEntity
    started_at: float = 0
    model_schemas: Optional[list[AIModelEntity]] = None

    model_config = ConfigDict(protected_namespaces=())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def validate_credentials(self, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self, params: dict = None) -> any:
        raise NotImplementedError

    def get_customizable_model_schema(self, model: str, credentials: dict) -> Optional[AIModelEntity]:
        return None

    def _get_default_parameter_rule_variable_map(self, name: DefaultParameterName) -> dict:

        default_parameter_rule = PARAMETER_RULE_TEMPLATE.get(name)

        if not default_parameter_rule:
            raise Exception(f"Invalid model parameter rule name {name}")

        return default_parameter_rule

    def get_customizable_model_schema_from_credentials(self, model: str, credentials: dict) -> Optional[AIModelEntity]:
        """
        Get customizable model schema from credentials

        :param model: model name
        :param credentials: model credentials
        :return: model schema
        """
        return self._get_customizable_model_schema(model, credentials)

    def _get_customizable_model_schema(self, model: str, credentials: dict) -> Optional[AIModelEntity]:
        """
        Get customizable model schema and fill in the template
        """
        schema = self.get_customizable_model_schema(model, credentials)

        if not schema:
            return None

        # fill in the template
        new_parameter_rules = []
        for parameter_rule in schema.parameter_rules:
            if parameter_rule.use_template:
                try:
                    default_parameter_name = DefaultParameterName.value_of(parameter_rule.use_template)
                    default_parameter_rule = self._get_default_parameter_rule_variable_map(default_parameter_name)
                    if not parameter_rule.max and "max" in default_parameter_rule:
                        parameter_rule.max = default_parameter_rule["max"]
                    if not parameter_rule.min and "min" in default_parameter_rule:
                        parameter_rule.min = default_parameter_rule["min"]
                    if not parameter_rule.default and "default" in default_parameter_rule:
                        parameter_rule.default = default_parameter_rule["default"]
                    if not parameter_rule.precision and "precision" in default_parameter_rule:
                        parameter_rule.precision = default_parameter_rule["precision"]
                    if not parameter_rule.required and "required" in default_parameter_rule:
                        parameter_rule.required = default_parameter_rule["required"]
                    if not parameter_rule.help and "help" in default_parameter_rule:
                        parameter_rule.help = I18nObject(
                            en_US=default_parameter_rule["help"]["en_US"],
                        )
                    if (
                            parameter_rule.help
                            and not parameter_rule.help.en_US
                            and ("help" in default_parameter_rule and "en_US" in default_parameter_rule["help"])
                    ):
                        parameter_rule.help.en_US = default_parameter_rule["help"]["en_US"]
                    if (
                            parameter_rule.help
                            and not parameter_rule.help.zh_Hans
                            and ("help" in default_parameter_rule and "zh_Hans" in default_parameter_rule["help"])
                    ):
                        parameter_rule.help.zh_Hans = default_parameter_rule["help"].get(
                            "zh_Hans", default_parameter_rule["help"]["en_US"]
                        )
                except ValueError:
                    pass

            new_parameter_rules.append(parameter_rule)

        schema.parameter_rules = new_parameter_rules

        return schema

    def predefined_models(self) -> list[AIModelEntity]:

        if self.model_schemas:
            return self.model_schemas

        model_schemas = []

        # get module name
        model_type = self.__class__.__module__.split(".")[-1]

        # get provider name
        provider_name = self.__class__.__module__.split(".")[-3]

        # 当前文件的绝对路径
        current_path = os.path.abspath(__file__)
        # print("current_path", current_path)
        # 获取当前文件所在目录的父目录（也就是上一级）
        base_path = os.path.dirname(os.path.dirname(current_path))  # 上一级
        # print("base_path", base_path)

        # 拼接目标路径：{base_path}/providers/{provider_name}/{model_type}
        provider_model_type_path = os.path.join(
            base_path, "providers", provider_name, model_type
        )
        # print("provider_model_type_path", provider_model_type_path)

        # get all yaml files path under provider_model_type_path that do not start with __
        model_schema_yaml_paths = [
            os.path.join(provider_model_type_path, model_schema_yaml)
            for model_schema_yaml in os.listdir(provider_model_type_path)
            if not model_schema_yaml.startswith("__")
               and not model_schema_yaml.startswith("_")
               and os.path.isfile(os.path.join(provider_model_type_path, model_schema_yaml))
               and model_schema_yaml.endswith(".yaml")
        ]

        # get _position.yaml file path
        position_map = get_position_map(provider_model_type_path)

        # traverse all model_schema_yaml_paths
        for model_schema_yaml_path in model_schema_yaml_paths:
            # read yaml data from yaml file
            yaml_data = load_yaml_file(model_schema_yaml_path)

            new_parameter_rules = []
            for parameter_rule in yaml_data.get("parameter_rules", []):
                if "use_template" in parameter_rule:
                    try:
                        default_parameter_name = DefaultParameterName.value_of(parameter_rule["use_template"])
                        default_parameter_rule = self._get_default_parameter_rule_variable_map(default_parameter_name)
                        copy_default_parameter_rule = default_parameter_rule.copy()
                        copy_default_parameter_rule.update(parameter_rule)
                        parameter_rule = copy_default_parameter_rule
                    except ValueError:
                        pass

                if "label" not in parameter_rule:
                    parameter_rule["label"] = {"zh_Hans": parameter_rule["name"], "en_US": parameter_rule["name"]}

                new_parameter_rules.append(parameter_rule)

            yaml_data["parameter_rules"] = new_parameter_rules

            if "label" not in yaml_data:
                yaml_data["label"] = {"zh_Hans": yaml_data["model"], "en_US": yaml_data["model"]}

            yaml_data["fetch_from"] = FetchFrom.PREDEFINED_MODEL.value

            try:
                # yaml_data to entity
                model_schema = AIModelEntity(**yaml_data)
            except Exception as e:
                model_schema_yaml_file_name = os.path.basename(model_schema_yaml_path).rstrip(".yaml")
                raise Exception(
                    f"Invalid model schema for {provider_name}.{model_type}.{model_schema_yaml_file_name}: {str(e)}"
                )

            # cache model schema
            model_schemas.append(model_schema)

        # resort model schemas by position
        model_schemas = sort_by_position_map(position_map, model_schemas, lambda x: x.model)

        # cache model schemas
        self.model_schemas = model_schemas

        return model_schemas
