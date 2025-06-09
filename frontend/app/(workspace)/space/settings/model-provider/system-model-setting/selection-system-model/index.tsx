import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  DropdownSection,
  Button,
  Input,
} from "@heroui/react";
import {ProviderModelWithStatusEntity, ProviderWithModels} from "@/app/api/model-provider/model";
import {ProviderIcon} from "../../components/provider-icon";
import {RenderFeatures} from "@/app/(workspace)/space/settings/model-provider/components/render-features";
import React, {useMemo, useState} from "react";

interface SelectionSystemModelProps {
  providersWithModels?: ProviderWithModels[];
  label: string;
  onSelect?: (provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => void;
  currentSelectValue?: string;
}

const SelectionSystemModel: React.FC<SelectionSystemModelProps> = ({
                                                                     providersWithModels = [],
                                                                     label,
                                                                     onSelect,
                                                                     currentSelectValue,
                                                                   }) => {
  const [selectedKey, setSelectedKey] = useState<string | undefined>(currentSelectValue);

  const [searchText, setSearchText] = useState("");

  const filteredProviders = useMemo(() => {
    if (!searchText.trim()) return providersWithModels;
    return providersWithModels
      .map((provider) => ({
        ...provider,
        models: provider.models.filter((model) =>
          model.label?.zh_Hans?.toLowerCase().includes(searchText.toLowerCase()) ||
          model.model?.toLowerCase().includes(searchText.toLowerCase())
        ),
      }))
      .filter((provider) => provider.models.length > 0);
  }, [providersWithModels, searchText]);

  const selectedModel = useMemo(() => {
    return providersWithModels
      .flatMap((p) => p.models.map((m) => ({...m, provider: p.provider})))
      .find((m) => m.model === selectedKey);
  }, [selectedKey, providersWithModels]);

  const handleSelectModel = (key: any) => {
    const stringKey = key.toString(); // 保证是 string 类型
    // console.log("选中模型的 key:", stringKey);

    setSelectedKey(stringKey); // ✅ 更新选中的 key

    // 遍历找出包含该模型的 provider 和模型
    for (const provider of providersWithModels) {
      const selectedModel = provider.models.find(m => m.model === stringKey);
      if (selectedModel && onSelect) {
        onSelect(provider, selectedModel); // ✅ 返回 provider 字符串 + 模型实体
        break;
      }
    }
  };

  const renderMenuItems = () => {
    if (filteredProviders.length === 0) {
      return (
        <DropdownItem key="no-result" isReadOnly className="text-default-400">
          未找到匹配的模型
        </DropdownItem>
      );
    }

    return filteredProviders.map((provider) => (
      <DropdownSection
        key={provider.provider}
        title={provider.label?.zh_Hans || provider.provider}
        showDivider
      >
        {provider.models.map((model) => {
          const isDisabled = model.status !== "active";
          return (
            <DropdownItem
              key={model.model}
              startContent={
                <ProviderIcon providerName={provider.provider} iconSize="icon_small"/>
              }
              className={isDisabled ? "opacity-50 pointer-events-none" : ""}
            >
              {model.label?.zh_Hans || model.model}
            </DropdownItem>
          );
        })}
      </DropdownSection>
    ));
  };

  return (
    <div className="w-full max-w-xl">
      <Dropdown>
        <div className="flex flex-col gap-2 px-2 mt-4">
          <span className="font-bold">{label}</span>
          <DropdownTrigger>
            <Button variant="bordered" className="w-full justify-between">
              {selectedModel ? (
                <div className="flex items-center gap-2">
                  <ProviderIcon providerName={selectedModel.provider} iconSize="icon_small"/>
                  <div className="flex flex-row text-left justify-center content-center w-full gap-2">
                    <div className="font-medium">{selectedModel.label?.zh_Hans || selectedModel.model}</div>
                    <div className="flex flex-row justify-center content-center text-xs text-default-400">
                      <RenderFeatures features={selectedModel.features}/>
                    </div>
                  </div>
                </div>
              ) : (
                "模型设置"
              )}
            </Button>
          </DropdownTrigger>
        </div>

        <DropdownMenu
          selectionMode="single"
          selectedKeys={selectedKey ? [selectedKey] : []}
          aria-label="Model Selection"
          variant="faded"
          className="min-w-[400px] max-h-[450px] overflow-auto p-2"
          onAction={(key) => handleSelectModel(key)}
          topContent={
            <div className="mb-2 px-1">
              <Input
                size="sm"
                variant="bordered"
                placeholder="搜索模型名称..."
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                className="w-full"
              />
            </div>
          }
        >
          {renderMenuItems()}
        </DropdownMenu>
      </Dropdown>
    </div>
  );
};

export default SelectionSystemModel;
