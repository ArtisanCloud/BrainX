"use client";

import useSettingsStore from "@/app/store/setting";
import styles from "./index.module.scss";
import {useState} from "react";
import React from "react";
import {ProviderIcon} from "../provider-icon";
import ModalSettingProvider from "../modal-setting-provider";
import ModalAddModels from "../modal-add-models";
import {IoIosArrowDown, IoIosArrowForward} from "react-icons/io";
import {ActionGetProviderModels, ProviderModel} from "@/app/api/model-provider/model";
import {useNotification} from "@/app/components/notification";
import {Checkbox, Switch} from "@heroui/react";


const ConfiguredProviders: React.FC = () => {
  const {configuredProviders, configuredProviderModels, setConfiguredProviderModels} = useSettingsStore(); // 获取 providers
  const [iconUrl, setIconUrl] = useState<string | null>(null);
  const [activeKeys, setActiveKeys] = useState<Record<string, boolean>>({});
  const [hoverKey, setHoverKey] = useState<string | boolean>(false);
  const [modelStatus,setModelStatus] = useState<Record<string, boolean>>({})
  const {msgError} = useNotification();

  // 检查 providers 是否为空或未定义
  if (!configuredProviders || Object.keys(configuredProviders).length === 0) {
    return <span className="text-lg font-semibold text-gray-500">
            请添加模型
          </span>; // 如果没有 providers，显示提示
  }

  const clickProviderModel = async (provider_id: string) => {
    if (configuredProviderModels[provider_id]) {
      setActiveKeys(prev => ({
        ...prev,
        [provider_id]: !prev[provider_id]
      }))
    } else {
      await loadModels(provider_id);
      setActiveKeys(prev => ({
        ...prev,
        [provider_id]: true
      }));
    }
  }

  const loadModels = async (provider_id: string) => {

    // 检查是否已经加载过模型
    const res = await ActionGetProviderModels({
      provider_id: provider_id,
    })
    if (res.data) {
      setConfiguredProviderModels(provider_id, res.data);
      for (let i = 0; i < res.data.length; i++) {
        setModelStatus(prev => ({
          ...prev,
          [res.data[i].model]: res.data[i].status
        }))
      }
    } else {
      msgError("获取模型失败");
    }

    return res.data
  }

  const setChangeModelStatus = async (model: ProviderModel) => {
    // const models = configuredProviderModels[provider_id];
    model.status = !model.status;
    // console.log(model.status);
    setModelStatus(prev => ({
      ...prev,
      [model.model]: model.status
    }))
  }

  return (
    <div className={styles.container}>
      {Object.entries(configuredProviders).map(([key, provider]) => {
        // 获取 provider 和 description 对应当前语言的值
        const providerName = provider.provider;
        const providerDescription = provider.description?.zh_Hans;
        // const providerBackgroundColor = provider.background || "#f5f5f5"; // 默认背景色
        const providerBackgroundColor =
          "linear-gradient(to right, #e0e0e0, #eee)";
        const supportedModelTypes = provider.supported_model_types || [];
        const models = configuredProviderModels[provider.provider] || [];
        const modelCount = models.length;
        const isActive = activeKeys[provider.provider];
        const isHover = hoverKey === provider.provider;
        const renderText = () => {
          if (modelCount === 0) return <>显示模型 <IoIosArrowForward/></>;
          if (!isActive && isHover) return <>显示 {modelCount} 个模型 <IoIosArrowForward/></>;
          if (isActive) return <>{modelCount} 个模型 <IoIosArrowDown/></>;
          return <>{modelCount} 个模型 <IoIosArrowForward/></>;
        };

        return (
          <div key={key} className={styles.providerItem} style={{background: providerBackgroundColor}}>
            <div className={styles.providerBox}>
              <div className={styles.providerLeft}>
                <div className="flex flex-col gap-2">
                  <h3>
                    {/* 服务端组件加载图片 */}
                    <ProviderIcon providerName={providerName}/>
                  </h3>
                  <div className="flex flex-wrap gap-0.5">
                    {Object.keys(supportedModelTypes).map((_, index: number) => (
                      <div className={styles.modelTypeTag} key={index}>
                        {supportedModelTypes[index]}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div className={styles.providerRight}>
                <ModalSettingProvider provider={provider}/>
              </div>
            </div>
            <div className={styles.modelsBox}>
              <div
                className={`w-full flex flex-col justify-between content-center ${isActive ? 'bg-white rounded-md' : 'border-t border-gray-300'}`}>
                <div className="flex flex-row w-full justify-between content-center p-2">
                <span
                  className={`${styles.btnShowModels} ${isActive ? styles.active : ""} ${isHover ? styles.hover : ""}`}
                  onClick={() => clickProviderModel(provider.provider)}
                  onMouseEnter={() => setHoverKey(provider.provider)}
                  onMouseLeave={() => setHoverKey(false)}
                >
                  {renderText()}
                </span>
                  <div><ModalAddModels provider={provider}/></div>
                </div>
                <div
                  className={`flex flex-col w-full gap-2 p-2 ${isActive ? '' : 'hidden'}`}
                >
                  {(configuredProviderModels[provider.provider] && isActive) &&
                    Object.entries(configuredProviderModels[provider.provider]).map(([modelIndex, model]) => (
                      <div key={`model-${modelIndex}`} className="flex flex-row w-full p-2 gap-2 hover:bg-gray-100 rounded-md">
                        <div className="flex flex-row justify-between content-center w-full gap-0.5">
                          <div className="flex flex-row items-center justify-center gap-2">
                            <div className="text-sm font-medium text-gray-900">
                              {model.label.zh_Hans}
                            </div>
                            <div className="flex flex-row text-sm font-normal leading-5">
                              {model.model_properties &&
                                Object.entries(model.model_properties).map(([key, value], index) => (
                                  <span key={index} className="mr-2 border-gray-400 border-1 rounded p-0.5 text-xs">
                                  {String(value)}
                                </span>
                                ))}
                            </div>
                          </div>
                          <div className="flex flex-row justify-center content-center">

                            <Switch isSelected={modelStatus[model.model]} size={"sm"} onValueChange={() => setChangeModelStatus(model )} />
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ConfiguredProviders;
