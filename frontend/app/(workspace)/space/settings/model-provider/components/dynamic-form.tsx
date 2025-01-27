import React, { useEffect, useState } from "react";
import { Input, Select, Radio, Switch, SelectItem, Form } from "@heroui/react"; // 替换为实际使用的 UI 库组件
import { CredentialForm } from "@/app/api/model-provider/provider";
import { FormOption, FormType } from "@/app/api/model-provider";

export default function DynamicForm({
  credentialSchemas,
  onFilledRequired, // 接收外部的回调函数
  onChange,
}: {
  credentialSchemas: CredentialForm[];
  onFilledRequired?: (filled: boolean) => void; // 回调函数的类型，可能为空
  onChange?: (formValues: Record<string, any>) => void;
}) {
  const [formValues, setFormValues] = useState<Record<string, any>>({});

  const handleChange = (variable: string, value: any) => {
    // console.log(variable, value);
    const updatedFormValues = {
      ...formValues,
      [variable]: value,
    };
    setFormValues(updatedFormValues);

    if (onChange) {
      onChange(updatedFormValues); // 实时传递表单值
    }
  };

  // 检查必填字段是否已填写
  const checkFilledRequired = () => {
    const filled = credentialSchemas.every((field) => {
      // 检查字段是必填并且已经有值
      return field.required === false || formValues[field.variable];
    });

    // 如果所有必填字段已填写，触发回调通知外部

    if (onFilledRequired) {
      onFilledRequired(filled);
    }
  };

  // 监听表单值变化，检查必填字段是否已填写
  useEffect(() => {
    checkFilledRequired();
  }, [formValues]);

  return (
    <>
      {credentialSchemas.map((field: CredentialForm) => {
        const isRequired = field.required !== false; // 默认为 true
        const placeholder =
          field.placeholder?.zh_CN ||
          field.placeholder?.en_US ||
          "Enter your value here"; // 示例支持多语言
        const title = field.title.zh_CN || field.title?.zh_CN || "Field"; // 示例支持多语言
        // console.log(field);
        // 根据字段类型动态渲染表单
        let inputElement;
        switch (field.type) {
          case FormType.INPUT_TEXT:
          case FormType.INPUT_SECRET:
            inputElement = (
              <Input
                errorMessage={
                  (isRequired && field.placeholder?.zh_CN) ||
                  field.placeholder?.en_US
                    ? "This field is required"
                    : ""
                }
                // type={field.type === FormType.INPUT_TEXT ? "text" : "password"}
                placeholder={placeholder}
                value={formValues[field.variable] || ""}
                maxLength={
                  field.max_length && field.max_length > 0
                    ? field.max_length
                    : 9999
                }
                onChange={(e) => handleChange(field.variable, e.target.value)}
              />
            );
            break;

          case FormType.SELECT:
            inputElement = (
              <Select
                placeholder={placeholder}
                items={field.options}
                onChange={(value) => handleChange(field.variable, value)} // 修复：使用箭头函数传递参数
              >
                {(option: FormOption) => (
                  <SelectItem>
                    {option.title.zh_CN || option.title.en_US}
                  </SelectItem>
                )}
              </Select>
            );
            break;

          case FormType.RADIO:
            inputElement = (
              <div className="flex flex-col">
                {field.options?.map((option) => (
                  <title key={option.value} className="flex items-center">
                    <Radio
                      name={field.variable}
                      value={option.value}
                      checked={formValues[field.variable] === option.value}
                      onChange={() =>
                        handleChange(field.variable, option.value)
                      }
                    />
                    <span className="ml-2">{option.title.zh_CN}</span>
                  </title>
                ))}
              </div>
            );
            break;

          case FormType.SWITCH:
            inputElement = (
              <Switch
                checked={!!formValues[field.variable]}
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
