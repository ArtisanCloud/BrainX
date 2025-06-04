import {CredentialForm, Provider} from "@/app/api/model-provider/provider";
import {FormType, MODEL_TYPE_TEXT, ModelTypeEnum} from "@/app/api/model-provider";

export function BuildMergedCredentialSchemas(provider: Provider): CredentialForm[] {

  const model_credential_schema = provider.model_credential_schema
  const model = model_credential_schema?.model!
  const supported_model_types = provider.supported_model_types
  const modelTypeField: CredentialForm = {
    variable: "__model_type",
    label: {
      zh_Hans: '模型类型',
      en_US: 'Model Type',
    },
    type: FormType.RADIO,
    required: true,
    default: supported_model_types[0],
    options: supported_model_types.map((modelType: ModelTypeEnum) => {
      return {
        value: modelType,
        label: {
          zh_Hans: MODEL_TYPE_TEXT[modelType],
          en_US: MODEL_TYPE_TEXT[modelType],
        },
        show_on: [],
      }
    }),
  };

  const modelField: CredentialForm = {
    variable: "model",
    label: model.label,         // 多语言标题
    type: FormType.INPUT_TEXT, // 假设是文本输入，可根据实际字段类型调整
    required: true,
    placeholder: model.placeholder, // 占位符
  };


  // const formValue = [modelTypeField, modelField, ...(model_credential_schema?.credential_form_schemas || [])];
  // console.log("formValue:", formValue);
  // return formValue;
  return [modelTypeField, modelField, ...(model_credential_schema?.credential_form_schemas || [])];
}
