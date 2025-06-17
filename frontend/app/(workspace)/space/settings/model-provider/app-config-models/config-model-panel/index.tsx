import styles from './index.module.scss';

import DynamicForm
  from "@/app/(workspace)/space/settings/model-provider/app-config-models/config-model-panel/dynamic-form";
import {useModelConfigStore} from "@/app/store/app/model-config";
import {Button, Divider} from "@heroui/react";
import {ArrowUturnLeftIcon} from "@heroicons/react/16/solid";


interface ConfigModelPanelProps {
}

const ConfigModelPanel: React.FC<ConfigModelPanelProps> = ({
                                                           }) => {
  const {params,providerModel, isPanelOpen, setPanelOpen} = useModelConfigStore();

  return (

    <div
      className={styles.container}
    >
      <div className='w-full flex flex-row justify-start items-center gap-2 p-2'>
        <Button isIconOnly size="sm" // 尽量选用 small
                className="w-6 h-6 p-1 min-w-0 min-h-0"
                onPress={() => setPanelOpen(false)}>
          <ArrowUturnLeftIcon className="w-4 h-4"/>
        </Button>
        <h3 className='text-sm font-medium'>
          {providerModel?.model}
        </h3>
      </div>
      <Divider className='mb-2'/>
      <DynamicForm
        params={params}
        language="zh_Hans"
        onChange={(form) => console.log("更新参数：", form)}
      />
    </div>
  )
}
export default ConfigModelPanel
