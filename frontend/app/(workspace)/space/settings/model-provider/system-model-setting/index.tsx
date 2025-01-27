import styles from './index.module.scss';
import {Button, Input, Popover, PopoverContent, PopoverTrigger} from "@heroui/react";
import {Cog6ToothIcon} from '@heroicons/react/24/outline';

const BrainXTemplateComponent: React.FC = () => {

  return (
    <div className={styles.container}>
      <Popover showArrow offset={10} placement="bottom">
        <PopoverTrigger>
          <Button
            className="flex items-center px-2 h-6 text-xs text-gray-700 cursor-pointer bg-gray-50 rounded-md border-[0.5px] border-gray-200 shadow-xs hover:bg-gray-100 hover:shadow-none false "
            color="default" startContent={<Cog6ToothIcon className="size-4 text-gray-400"/>}>设置系统模型</Button>
        </PopoverTrigger>
        <PopoverContent className="w-[240px]">
          {(titleProps) => (
            <div className="px-1 py-2 w-full">
              <p className="text-small font-bold text-foreground" {...titleProps}>
                Dimensions
              </p>
              <div className="mt-2 flex flex-col gap-2 w-full">
                <Input defaultValue="100%" label="Width" size="sm" variant="bordered"/>
                <Input defaultValue="300px" label="Max. width" size="sm" variant="bordered"/>
                <Input defaultValue="24px" label="Height" size="sm" variant="bordered"/>
                <Input defaultValue="30px" label="Max. height" size="sm" variant="bordered"/>
              </div>
            </div>
          )}
        </PopoverContent>
      </Popover>
    </div>
  )
}
export default BrainXTemplateComponent
