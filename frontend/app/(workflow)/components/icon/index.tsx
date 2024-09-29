import {
  ApiOutlined,
  RetweetOutlined,
  ApartmentOutlined,
  MessageOutlined,
  DatabaseOutlined,
} from '@ant-design/icons'; // 确保替换为你实际使用的图标库或组件

import {
  LightBulbIcon,
  CodeBracketIcon,
  AcademicCapIcon,
  CogIcon,
  CubeTransparentIcon,
} from '@heroicons/react/24/outline';

const size = 28
// 图标映射对象
export const iconMapping = {
  plugin: {
    component: ApiOutlined,
    size: size,
    backgroundColor: "#3b77d2"  // 自定义背景颜色
  },
  llm: {
    component: LightBulbIcon,
    size: size,
    backgroundColor: "#080f11"
  },
  code: {
    component: CodeBracketIcon,
    size: size,
    backgroundColor: "#31a9a5"
  },
  knowledge: {
    component: AcademicCapIcon,
    size: size,
    backgroundColor: "#ce1345"
  },
  workflow: {
    component: ApartmentOutlined,
    size: size,
    backgroundColor: "#58de21"
  },
  condition: {
    component: CubeTransparentIcon,
    size: size,
    backgroundColor: "#d77e4d"
  },
  loop: {
    component: RetweetOutlined,
    size: size,
    backgroundColor: "#7a36e0"
  },
  message: {
    component: MessageOutlined,
    size: size,
    backgroundColor: "#d9bf39"
  },
  database: {
    component: DatabaseOutlined,
    size: size,
    backgroundColor: "#cb5e10"
  },
  // 可以根据需要继续添加其他图标
};
