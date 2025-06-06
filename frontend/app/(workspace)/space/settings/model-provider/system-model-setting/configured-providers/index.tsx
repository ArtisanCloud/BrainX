"use client";

import useSettingsStore from "@/app/store/setting";
import styles from "./index.module.scss";
import {useState} from "react";
import React from "react";
import {ProviderIcon} from "../provider-icon";
import {IoIosArrowDown, IoIosArrowForward} from "react-icons/io";
import {
  ActionChangeModelStatus,
  ActionGetModelCredentials,
  ActionGetProviderModels,
  ProviderModel
} from "@/app/api/model-provider/model";
import {useNotification} from "@/app/components/notification";
import {Button, Switch} from "@heroui/react";
import {CogIcon} from "@heroicons/react/24/outline";
import {FaCirclePlus} from "react-icons/fa6";
import {GrStatusGoodSmall} from "react-icons/gr";
import {
  ActionGetProviderCredentials,
  ConfigurateMethod,
  CustomConfigurationStatusEnum,
  Provider
} from "@/app/api/model-provider/provider";


const ConfiguredProviders: React.FC = () => {
  const {
    configuredProviders, setCurrentProvider, setCurrentModel,
    configuredProviderModels, setConfiguredProviderModels,
    setIsOpenSaveModelModal, setIsOpenSaveProviderModal,
    setFormValues,
  } = useSettingsStore(); // 获取 providers
  const [iconUrl, setIconUrl] = useState<string | null>(null);
  const [activeKeys, setActiveKeys] = useState<Record<string, boolean>>({});
  const [hoverKey, setHoverKey] = useState<string | boolean>(false);
  const [modelStatus, setModelStatus] = useState<Record<string, boolean>>({})
  const {msgError} = useNotification();

  // 检查 providers 是否为空或未定义
  if (!configuredProviders || Object.keys(configuredProviders).length === 0) {
    return <span className="text-lg font-semibold text-gray-500">
            请添加模型
          </span>; // 如果没有 providers，显示提示
  }

  const onClickShowModels = async (provider_id: string) => {
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
          [res.data[i].model]: res.data[i].status === "active"
        }))
      }
    } else {
      msgError("获取模型失败");
    }

    return res.data
  }


  const setChangeModelStatus = async (provider: string, model: ProviderModel) => {
    const changeToStatus = !(model.status === "active")
    const res = await ActionChangeModelStatus({
      provider: provider,
      model_type: model.model_type,
      model: model.model,
      status: changeToStatus
    })

    if (res.result) {
      model.status = "inactive"
      // console.log(model.status);
      setModelStatus(prev => ({
        ...prev,
        [model.model]: changeToStatus
      }))
    } else {
      msgError("切换模型状态失败");
    }
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

        const onClickToSaveProvider = async (provider: Provider) => {
          setCurrentProvider(provider)

          if (provider.custom_configuration.status === CustomConfigurationStatusEnum.active) {
            const res = await ActionGetProviderCredentials({
              provider: provider.provider,
            })
            if (res.data) {
              setFormValues(res.data);
            }
          }
          setIsOpenSaveProviderModal(true);
        }
        const onClickToSaveModel =async (provider: Provider, model: ProviderModel | null) => {
          setCurrentProvider(provider)
          if (model) {
            setCurrentModel(model)
            const res = await ActionGetModelCredentials({
              provider: provider.provider,
              model_type: model.model_type,
              model: model.model,
            })
            if (res.data) {
              setFormValues(res.data);
            }
          }
          setIsOpenSaveModelModal(true);
        }

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
                <div className={styles.actionBox}>
                  <div className={styles.statusBox}>
                    <span>API-KEY</span>
                    <GrStatusGoodSmall style={{border: "1px solid white", borderRadius: 48}} color="green"/>
                  </div>
                  {provider.configurate_methods.includes(ConfigurateMethod.PREDEFINED_MODEL) &&
                  <Button
                    key={provider.provider}
                    className={styles.btnFun}
                    startContent={<CogIcon style={{width: "12px", color: "gray"}}/>}
                    onPress={() => onClickToSaveProvider(provider)}
                  >
                    设置
                  </Button>
                  }
                </div>
              </div>
            </div>
            <div className={styles.modelsBox}>
              <div
                className={`w-full flex flex-col justify-between content-center ${isActive ? 'bg-white rounded-md' : 'border-t border-gray-300'}`}>
                <div className="flex flex-row w-full justify-between content-center p-2">
                <span
                  className={`${styles.btnShowModels} ${isActive ? styles.active : ""} ${isHover ? styles.hover : ""}`}
                  onClick={() => onClickShowModels(provider.provider)}
                  onMouseEnter={() => setHoverKey(provider.provider)}
                  onMouseLeave={() => setHoverKey(false)}
                >
                  {renderText()}
                </span>
                  <div>
                    <Button
                      key={provider.provider}
                      className={styles.btnFunActive}
                      startContent={<FaCirclePlus style={{width: "12px", color: "gray"}}/>}
                      onPress={() => onClickToSaveModel(provider, null)}
                    >
                      添加模型
                    </Button>
                  </div>
                </div>
                <div
                  className={`flex flex-col w-full gap-2 p-2 ${isActive ? '' : 'hidden'}`}
                >
                  {(configuredProviderModels[provider.provider] && isActive) &&
                    Object.entries(configuredProviderModels[provider.provider]).map(([modelIndex, model]) => (
                      <div key={`model-${modelIndex}`}
                           className="flex flex-row w-full p-2 gap-2 hover:bg-gray-100 rounded-md">
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
                          <div className="flex flex-row justify-center content-center gap-2">
                            {!provider.configurate_methods.includes(ConfigurateMethod.PREDEFINED_MODEL) &&
                              <Button
                                key={`btn-config-${modelIndex}`}
                                size="sm"
                                className="border-gray-400 border-1 rounded p-0.5 text-xs bg-white opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                                startContent={<CogIcon style={{width: "12px", color: "gray"}}/>}
                                onPress={() => onClickToSaveModel(provider, model)}
                              >配置</Button>
                            }
                            <Switch
                              isSelected={modelStatus[model.model]}
                              size={"sm"}
                              onValueChange={() => setChangeModelStatus(provider.provider, model)}/>
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
