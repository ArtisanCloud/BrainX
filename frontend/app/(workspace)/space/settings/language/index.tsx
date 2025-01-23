import styles from './index.module.scss';
import {Select} from "@heroui/select";
import {SelectItem} from "@heroui/react";

type Option = {
  key: string;
  label: string;
};

const languages: Option[] = [
  { key: "en", label: "English (英语)" },
  { key: "zh", label: "简体中文 (Simplified Chinese)" },
  { key: "zh-tw", label: "繁體中文 (Traditional Chinese)" },
  { key: "fr", label: "Français (French)" },
  { key: "de", label: "Deutsch (German)" },
  { key: "es", label: "Español (Spanish)" },
  { key: "ja", label: "日本語 (Japanese)" },
  { key: "ko", label: "한국어 (Korean)" },
  { key: "ru", label: "Русский (Russian)" },
  { key: "ar", label: "العربية (Arabic)" },
];

const timezones: Option[] = [
  { key: "utc-12", label: "国际日期变更线西 (UTC-12)" },
  { key: "utc-11", label: "中途岛标准时间 (UTC-11)" },
  { key: "utc-10", label: "夏威夷标准时间 (Hawaii, UTC-10)" },
  { key: "utc-9", label: "阿拉斯加标准时间 (Alaska, UTC-9)" },
  { key: "utc-8", label: "太平洋标准时间 (PST, UTC-8)" },
  { key: "utc-7", label: "山区标准时间 (MST, UTC-7)" },
  { key: "utc-6", label: "中部标准时间 (CST, UTC-6)" },
  { key: "utc-5", label: "东部标准时间 (EST, UTC-5)" },
  { key: "utc+0", label: "格林威治标准时间 (GMT, UTC+0)" },
  { key: "utc+1", label: "中欧标准时间 (CET, UTC+1)" },
  { key: "utc+3", label: "莫斯科时间 (MSK, UTC+3)" },
  { key: "utc+5:30", label: "印度标准时间 (IST, UTC+5:30)" },
  { key: "utc+8", label: "中国标准时间 (CST, UTC+8, 北京/上海)" },
  { key: "utc+9", label: "日本标准时间 (JST, UTC+9)" },
  { key: "utc+10", label: "澳大利亚东部标准时间 (AEST, UTC+10)" },
  { key: "utc+12", label: "新西兰时间 (NZST, UTC+12)" },
];
const LanguageComponent: React.FC = () => {

  return (
    <div className={styles.container}>
      <Select
        className="max-w-xs"
        items={languages}
        label="语言"
        defaultSelectedKeys={["zh"]}
        placeholder="请选择语言"
      >
        {(language) => <SelectItem>{language.label}</SelectItem>}
      </Select>
      <Select
        className="max-w-xs"
        items={timezones}
        label="时差"
        defaultSelectedKeys={["utc+8"]}
        placeholder="请选择时差"
      >
        {(timezone) => <SelectItem>{timezone.label}</SelectItem>}
      </Select>
    </div>
  )
}
export default LanguageComponent
