// 先定义一个特征对应图标的映射对象
import {ModelFeature, ModelFeatureText} from "@/app/api/model-provider";
import {
  ChatBubbleOvalLeftEllipsisIcon,
  WrenchIcon, WrenchScrewdriverIcon,
  LightBulbIcon, EyeIcon
} from "@heroicons/react/16/solid";
import {Tooltip} from "@heroui/react";


const iconClass = "rounded w-4 h-4 border border-gray-400"
const featureIconMap: Record<ModelFeature, () => React.ReactNode> = {
  [ModelFeature.TOOL_CALL]: () => <WrenchIcon className={iconClass}/>,
  [ModelFeature.MULTI_TOOL_CALL]: () => <WrenchScrewdriverIcon className={iconClass}/>,
  [ModelFeature.AGENT_THOUGHT]: () => <LightBulbIcon className={iconClass}/>,
  [ModelFeature.VISION]: () => <EyeIcon className={iconClass}/>,
  [ModelFeature.STREAM_TOOL_CALL]: () => <ChatBubbleOvalLeftEllipsisIcon className={iconClass}/>,
};


export const RenderFeatures: React.FC<{ features?: string[] }> = ({features}) => {
  if (!features || features.length === 0) return null;

  return (
    <div className="flex flex-row justify-center content-center gap-2 flex-wrap">
      {features.map((feature) => {
        // console.log(feature)
        const Icon = featureIconMap[feature as ModelFeature];
        return (
          <div key={feature} className="flex items-center gap-1 text-xs text-default-400">
            <Tooltip content={ModelFeatureText[feature as keyof typeof ModelFeatureText]}>
              {Icon ? Icon() : null}
            </Tooltip>
          </div>
        );
      })}
    </div>
  );
};

