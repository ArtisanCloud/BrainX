import { ProviderModel } from "@/app/api/model-provider/model";
import { Select, SelectItem, Avatar } from "@heroui/react";
interface SelectionSystemModelProps {
  models?: ProviderModel[]; // models 变为可选
  label: string; // 占位符文本
  onSelect?: (model: ProviderModel) => void; // 可选的回调函数
  currentSelectValue?: string; // 当前选中的模型 id
}

const SelectionSystemModel: React.FC<SelectionSystemModelProps> = ({
  models = [], // 默认值为空数组
  label,
  onSelect,
  currentSelectValue,
}) => {
  return (
    <div className="max-w-xs">
      <Select
        value={currentSelectValue}
        onChange={(event) => {
          const selectedValue = event.target.value; // 获取选择的值
          const selectedModel = models.find(
            (model) => model.model === selectedValue
          );
          if (selectedModel && onSelect) onSelect(selectedModel);
        }}
        label={label} // 可根据需要翻译 "Select a model"
        labelPlacement="outside"
      >
        {models.map((model) => (
          <SelectItem
            key={model.model}
            value={model.model}
            textValue={model.label.zh_Hans}
          >
            <div className="flex gap-2 items-center">
              <Avatar alt={model.model} className="flex-shrink-0" size="sm" />
              <div className="flex flex-col">
                <span className="text-small">{model.label.zh_Hans}</span>
                <span className="text-tiny text-default-400">
                  {model.model_type}
                </span>
              </div>
            </div>
          </SelectItem>
        ))}
      </Select>
    </div>
  );
};

export default SelectionSystemModel;
