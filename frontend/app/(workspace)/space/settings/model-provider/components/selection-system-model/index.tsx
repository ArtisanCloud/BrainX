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
import {ProviderIcon} from "../provider-icon";
import {RenderFeatures} from "@/app/(workspace)/space/settings/model-provider/components/render-features";
import React, {useEffect, useMemo, useState} from "react";
import {CogIcon} from "@heroicons/react/24/outline";

interface SelectionSystemModelProps {
  providersWithModels?: ProviderWithModels[];
  label?: string;
  onSelect?: (provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => void;
  currentSelectValue?: string;
  initShowConfig?: boolean;
  onToConfig?: (provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => void;
}

const SelectionSystemModel: React.FC<SelectionSystemModelProps> = ({
                                                                     providersWithModels = [],
                                                                     label,
                                                                     onSelect,
                                                                     currentSelectValue,
                                                                     initShowConfig = false,
                                                                     onToConfig,
                                                                   }) => {
  const [selectedKey, setSelectedKey] = useState<string | undefined>(currentSelectValue);

  const [searchText, setSearchText] = useState("");
  const [showConfigMap, setShowConfigMap] = useState<Record<string, boolean>>({});

  const handleMouseEnterItem = (provider: string, modelKey: string) => {
    setShowConfigMap(prev => ({...prev, [provider + '-' + modelKey]: true}));
  };
  const handleMouseLeaveItem = (provider: string, modelKey: string) => {
    setShowConfigMap(prev => ({...prev, [provider + '-' + modelKey]: false}));
  };

  // ======================================================================

  useEffect(() => {
    setSelectedKey(currentSelectValue)
  }, [currentSelectValue])

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
    const flatModels = providersWithModels
      .flatMap((p) => p.models.map((m) => ({...m, provider: p.provider})));

    // console.log("selectedModel useMemo - flatModels:", flatModels); // Check all models
    // console.log("selectedModel useMemo - selectedKey:", selectedKey); // Check what's being searched for

    const foundModel = flatModels.find((m) => m.model === selectedKey);
    // console.log("selectedModel useMemo - foundModel:", foundModel); // Is it undefined?

    return foundModel;
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

  const handleToConfig = (provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => {
    if (onToConfig) {
      onToConfig(provider, model);
      handleMouseLeaveItem(provider.provider, model.model)
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
          // Create a unique key for each item's hover state
          const itemKey = `${provider.provider}-${model.model}`;
          // Get the show state for the current item from the map
          const showConfigForThisItem = showConfigMap[itemKey] || false;

          return (
            <DropdownItem
              key={model.model}
              startContent={
                <ProviderIcon providerName={provider.provider} iconSize="icon_small"/>
              }
              textValue={model.model}
              className={isDisabled ? "opacity-50 pointer-events-none" : ""}
              onMouseEnter={() => handleMouseEnterItem(provider.provider, model.model)}
              onMouseLeave={() => handleMouseLeaveItem(provider.provider, model.model)}
            >
              <div
                onClick={(e) => {
                  const target = e.target as HTMLElement;
                  if (target.closest(".cog-icon-button")) {
                    // 点击了齿轮，忽略选择
                    return;
                  }
                  handleSelectModel(model.model);
                }}
                className={`flex flex-row items-center gap-2 ${showConfigForThisItem ? 'justify-between' : 'justify-start'}`}>
                <span>{model.label?.zh_Hans || model.model}</span>
                {/* 在内容末尾添加按钮 */}

                {showConfigForThisItem && !isDisabled && (
                  <button
                    className="cog-icon-button"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      handleToConfig(provider, model);
                    }}
                  >
                    <CogIcon className="text-sm w-6 cursor-pointer"/>
                  </button>
                )}
              </div>
            </DropdownItem>
          );
        })}
      </DropdownSection>
    ));
  };

  return (
    <div className="w-full max-w-xl">
      <Dropdown>
        <div className="flex flex-col">
          {label && (
            <span className="text-default-400 text-sm mb-1">{label}</span>
          )}
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
