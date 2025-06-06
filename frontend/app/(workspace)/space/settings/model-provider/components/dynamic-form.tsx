import React, {useEffect, useState} from "react";
import {
  Input,
  Select,
  Radio,
  Switch,
  SelectItem,
  RadioGroup,
  cn,
} from "@heroui/react";
import {CredentialForm} from "@/app/api/model-provider/provider";
import {
  FormOption as DynamicFormOption,
  FormType,
} from "@/app/api/model-provider";

const SECRET_PLACEHOLDER = "*****"; // 展示给用户的占位
const SECRET_UPLOAD_PLACEHOLDER = "[__HIDDEN__]"; // 提交给后端的默认标记值


export default function DynamicForm({
                                      credentialSchemas,
                                      value,
                                      onFilledRequired,
                                      onChange,
                                    }: {
  credentialSchemas: CredentialForm[];
  onFilledRequired?: (filled: boolean) => void;
  value?: Record<string, any>;
  onChange?: (formValues: Record<string, any>) => void;
}) {
  const [formValues, setFormValues] = useState<Record<string, any>>({});

  const handleChange = (variable: string, value: any) => {
    const updatedFormValues = {
      ...formValues,
      [variable]: value,
    };
    // console.log(updatedFormValues);
    setFormValues(updatedFormValues);
    onChange?.(updatedFormValues);
  };

  // 获取字段当前值，兼容对象情况（value: string | { value: string, ... }）
  const getFieldValue = (variable: string) => {
    const val = formValues[variable];
    return typeof val === "object" && val !== null && "value" in val
      ? val.value
      : val;
  };

  function getDefaultSelectedKeys(field: CredentialForm): string[] {
    if (!field.options || !field.default) return [];

    const match = field.options.find(opt => opt.value === field.default);
    return match ? [match.value] : [];
  }

  const checkFilledRequired = () => {
    const filled = credentialSchemas?.every((field) => {
      // 如果字段未满足 show_on 条件，就忽略校验
      if (field.show_on && field.show_on.length > 0) {
        const shouldShow = field.show_on.every((condition) => {
          const currentValue = getFieldValue(condition.variable);
          return currentValue === condition.value;
        });
        if (!shouldShow) return true; // 忽略隐藏字段
      }

      // 校验 required 字段是否有值
      return field.required === false || getFieldValue(field.variable);
    });
    // console.log("filled:", filled);

    onFilledRequired?.(filled);
  };

  useEffect(() => {
    checkFilledRequired();
  }, [formValues]);

  useEffect(() => {
    const initialValues: Record<string, any> = {};

    credentialSchemas?.forEach((field) => {
      if (!field) return;
      const variable = field.variable;
      // console.log("field:", field);
      // console.log("variable:", variable);
      // console.log(value)
      // 优先使用外部传入的值
      if (value && value[variable] !== undefined) {
        // console.log("value[variable]:",value[variable])
        if (field.type === FormType.INPUT_SECRET) {
          initialValues[variable] = SECRET_UPLOAD_PLACEHOLDER;
        } else {
          initialValues[variable] = value[variable];
          if (variable=='model'){
            field.editable = false;
          }
        }
        return;
      }

      if (
        (field.type === FormType.SELECT) &&
        field.options &&
        field.options.length > 0
      ) {
        initialValues[variable] = field.default;
      }

      if (
        (field.type === FormType.RADIO) &&
        field.options &&
        field.options.length > 0
      ) {
        initialValues[variable] = field.default;
      }

      if (field.type === FormType.SWITCH) {
        initialValues[variable] = field.default; // switch 默认为 false
      }

      if (field.type === FormType.INPUT_TEXT || field.type === FormType.INPUT_SECRET) {
        initialValues[variable] = field.default;
      }
    });

    if (Object.keys(initialValues).length > 0) {
      setFormValues((prev) => ({...initialValues, ...prev}));
    }
  }, [credentialSchemas]);

  return (
    <>
      {credentialSchemas?.map((field: CredentialForm | undefined) => {
        if (!field) {
          return (
            <p key={Math.random()} className="text-red-500">
              Invalid field data
            </p>
          );
        }

        // ✅ 判断 show_on 条件
        if (field.show_on && field.show_on.length > 0) {
          const shouldShow = field.show_on.every((condition) => {
            const currentValue = getFieldValue(condition.variable);
            return currentValue === condition.value;
          });
          if (!shouldShow) return null;
        }

        const isRequired = field.required !== false;
        const placeholder =
          field.placeholder?.zh_Hans ||
          field.placeholder?.en_US ||
          "Enter your value here";
        const title = field.label?.zh_Hans || field.label?.en_US || "Field";

        let inputElement;

        switch (field.type) {
          case FormType.INPUT_TEXT:
            inputElement = (
              <Input
                errorMessage={
                  isRequired &&
                  !getFieldValue(field.variable) &&
                  "This field is required"
                }
                placeholder={placeholder}
                value={getFieldValue(field.variable) || ""}
                maxLength={field.max_length && field.max_length > 0 ? field.max_length : 9999}
                onChange={(e) => handleChange(field.variable, e.target.value)}
                isDisabled={field.editable === false}
              />
            );
            break;
          case FormType.INPUT_SECRET:
            inputElement = (
              <Input
                errorMessage={
                  isRequired &&
                  !getFieldValue(field.variable) &&
                  "This field is required"
                }
                type={"password"}
                placeholder={placeholder}
                value={getFieldValue(field.variable) || ""}
                maxLength={field.max_length && field.max_length > 0 ? field.max_length : 9999}
                onChange={(e) => handleChange(field.variable, e.target.value)}
              />
            );
            break;
          case FormType.SELECT:
            // console.log("字段名:", field.variable, "当前值:", getFieldValue(field.variable), "options:", field.options);
            inputElement = (
              <Select
                placeholder={placeholder}
                aria-label={title}
                items={field.options!}
                defaultSelectedKeys={getDefaultSelectedKeys(field)}
                onSelectionChange={(key) => handleChange(field.variable, key.currentKey)} // ✅ React Aria 风格的回调
              >

                {(option: DynamicFormOption) => (
                  <SelectItem key={option.value}>
                    {option.label.zh_Hans || option.label.en_US}
                  </SelectItem>
                )}
              </Select>
            );
            break;

          case FormType.RADIO:
            inputElement = (
              <div className="flex flex-row gap-4">
                <RadioGroup
                  orientation="horizontal"
                  value={formValues[field.variable] ?? ""}
                  onValueChange={(value) => {
                    // ✅ 使用 onValueChange 替代 onChange
                    handleChange(field.variable, value);
                  }}
                >
                  {field?.options?.map((option) => (
                    <Radio
                      key={option.value}
                      value={option.value}
                      classNames={{
                        base: cn(
                          "inline-flex m-0 bg-content1 hover:bg-content2 items-center justify-between",
                          "flex-row-reverse max-w-[300px] cursor-pointer rounded-lg gap-4 p-4 border-2 border-transparent",
                          "data-[selected=true]:border-primary",
                        ),
                      }}
                    >
                      {option.label.zh_Hans || option.label.en_US}
                    </Radio>
                  ))}
                </RadioGroup>
              </div>
            );
            break;

          case FormType.SWITCH:
            inputElement = (
              <Switch
                checked={!!getFieldValue(field.variable)}
                onChange={(checked) => handleChange(field.variable, checked)}
              />
            );
            break;

          default:
            inputElement = (
              <p className="text-red-500">Unsupported field type</p>
            );
        }

        return (
          <div key={field.variable} className="py-3">
            <div className="flex items-center py-2 text-sm text-gray-900">
              {title} {isRequired && <span className="text-red-500">*</span>}
            </div>
            <div className="ml-1">{inputElement}</div>
          </div>
        );
      })}
    </>
  );
}
