from abc import abstractmethod
from collections.abc import Mapping
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.runtime.defaults import PARAMETER_RULE_TEMPLATE
from app.core.brainx.entity.runtime.provider_model import ModelType, DefaultParameterName, AIModelEntity


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
