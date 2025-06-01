"use client";

import useSettingsStore from "@/app/store/setting";
import styles from "./index.module.scss";
import {useState} from "react";
import React from "react";
import {ProviderIcon} from "../provider-icon";
import ModalSettingProvider from "../modal-setting-provider";
import ModalAddModels from "../modal-add-models";

const ConfiguredProviders: React.FC = () => {
  const {configuredProviders} = useSettingsStore(); // 获取 providers
  const [iconUrl, setIconUrl] = useState<string | null>(null);

  // 检查 providers 是否为空或未定义
  if (!configuredProviders || Object.keys(configuredProviders).length === 0) {
    return <span className="text-lg font-semibold text-gray-500">
            请添加模型
          </span>; // 如果没有 providers，显示提示
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
              <div>显示模型</div>
              <div><ModalAddModels provider={provider}/></div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ConfiguredProviders;
