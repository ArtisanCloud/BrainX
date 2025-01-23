"use client";
import {Listbox, ListboxSection, ListboxItem, cn} from "@heroui/react";
import styles from './index.module.scss';
import {CubeIcon, UserGroupIcon, CircleStackIcon, PuzzlePieceIcon, LanguageIcon} from '@heroicons/react/24/outline'
import {ListBoxWrapper} from "@/app/(workspace)/space/settings/list-box-warpper";
import {PressEvent} from "@react-types/shared";
import {useState} from "react";
import useSettingsStore from "@/app/store/setting";
import ModelProvider from "@/app/(workspace)/space/settings/model-provider";
import Language from "@/app/(workspace)/space/settings/language";

// 定义 Item 和 Section 的类型
type Item = {
  key: string;
  label: string;
  value: React.ReactNode; // 支持所有可渲染的 JSX 节点
  icon: React.FC<React.SVGProps<SVGSVGElement>>; // 更加精确的类型
};

type Section = {
  title: string;
  items: Item[];
};

const SettingPage: React.FC = () => {


  const [selectedItem, setSelectedItem] = useState<Item>({
    key: "language",
    label: "语言",
    value: <Language/>,
    icon: LanguageIcon,
  });

  const settingStore = useSettingsStore()

  const iconClasses = "w-4 h-4 text-default-500 pointer-events-none flex-shrink-0"; // w-6 和 h-6 表示宽高为 1.5rem (24px)

  // 定义数据结构
  const sections: Section[] = [
    {
      title: "工作台",
      items: [
        {
          key: "provider",
          label: "模型提供商",
          value: <ModelProvider/>,
          icon: CubeIcon,
        },
        // {
        //   key: "team",
        //   label: "成员",
        //   icon: <UserGroupIcon className={iconClasses}/>,
        // },
        // {
        //   key: "datasource",
        //   label: "数据源",
        //   icon: <CircleStackIcon className={iconClasses}/>,
        // },
        // {
        //   key: "api",
        //   label: "API 扩展",
        //   icon: <PuzzlePieceIcon className={iconClasses}/>,
        // },
      ],
    },
    {
      title: "通用",
      items: [
        {
          key: "language",
          label: "语言",
          value: <Language/>,
          icon: LanguageIcon,
        },
      ]
    }
  ];


  const selectMenu = (item: Item) => {

    // console.log("Selected item:", item);
    setSelectedItem(item);
    if (item.key == "language") {
      settingStore.language = "123321"
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.box}>
        <div className={styles.navbarBox}>
          <div className={styles.navTop}>
            <p>设置</p>
          </div>
          <div className={styles.navBody}>
            <ListBoxWrapper>
              <Listbox aria-label="Listbox menu with icons" variant="faded">
                {sections.map((section) => (
                  <ListboxSection
                    key={section.title}
                    // showDivider
                    title={section.title}
                  >
                    {section.items.map((item) => {
                      const Icon = item.icon; // 动态获取组件
                      return (
                        <ListboxItem
                          key={item.key}
                          onPress={() => selectMenu(item)}
                          startContent={<Icon className={iconClasses}/>} // 动态渲染组件
                        >
                          {item.label}
                        </ListboxItem>
                      );
                    })}
                  </ListboxSection>
                ))}
              </Listbox>
            </ListBoxWrapper>
          </div>
        </div>
        <div className={styles.content}>
            <div className={styles.title}>{selectedItem.label}</div>
            <div className={styles.component}></div>
            {selectedItem.value}
        </div>
      </div>
    </div>
  )
}
export default SettingPage
