"use client";

import useSettingsStore from "@/app/store/setting";
import styles from "./index.module.scss";
import { useState } from "react";
import { ProviderIcon } from "./provider-icon";
import ModalAddModels from "@/app/(workspace)/space/settings/model-provider/system-model-setting/to-config-providers/modal-add-models";
import ModalSettingProvider from "@/app/(workspace)/space/settings/model-provider/system-model-setting/to-config-providers/modal-setting-provider";
import React from "react";

const ToConfigProviders: React.FC = () => {
  const { providers } = useSettingsStore(); // 获取 providers
  const [iconUrl, setIconUrl] = useState<string | null>(null);

  // 检查 providers 是否为空或未定义
  if (!providers || Object.keys(providers).length === 0) {
    return <div>No providers available</div>; // 如果没有 providers，显示提示
  }

  return (
    <div className={styles.container}>
      {Object.entries(providers).map(([key, provider]) => {
        // 获取 provider 和 description 对应当前语言的值
        const providerName = provider.provider;
        const providerDescription = provider.description?.zh_Hans;
        // const providerBackgroundColor = provider.background || "#f5f5f5"; // 默认背景色
        const providerBackgroundColor =
          "linear-gradient(to right, #e0e0e0, #eee)";
        const supportedModelTypes = provider.supported_model_types || [];

        const actionButtons = [
          {
            key: provider.provider + "-setting-provider",
            type: "providerSetting",
            component: <ModalSettingProvider provider={provider} />,
          },
          {
            key: provider.provider + "-add-models",
            type: "modelSetting",
            component: <ModalAddModels provider={provider} />,
          },
        ];

        // 过滤出需要显示的按钮
        const visibleButtons = actionButtons.filter((button) => {
          if (
            (button.type === "providerSetting" &&
              provider.provider_credential_schema) ||
            (button.type === "modelSetting" &&
              provider.models_credential_schema)
          ) {
            // console.log(provider.provider,button.type,provider.provider_credential_schema,provider.models_credential_schema )

            return true; // 显示按钮
          }
          return false; // 不显示按钮
        });
        // 根据按钮数量动态设置 grid-cols
        const gridCols =
          visibleButtons.length === 1 ? "grid-cols-1" : "grid-cols-2";

        return (
          <div
            key={key}
            className={`group ${styles.providerItem}`}
            style={{ background: providerBackgroundColor }}
          >
            <div className="flex-col">
              <h3>
                {/* 服务端组件加载图片 */}
                <ProviderIcon providerName={providerName} />
              </h3>
              <p className="mt-1 leading-4 text-xs text-black/[48] line-clamp-4">
                {providerDescription}
              </p>
            </div>
            <div className="shrink-0">
              <div className="flex flex-wrap group-hover:hidden gap-0.5">
                {Object.keys(supportedModelTypes).map((_, index: number) => (
                  <div className={styles.modelTypeTag} key={index}>
                    {supportedModelTypes[index]}
                  </div>
                ))}
              </div>
              <div className={`hidden group-hover:grid ${gridCols} gap-1`}>
                {visibleButtons.map((button) => (
                  <React.Fragment key={button.key}>
                    {button.component}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ToConfigProviders;
