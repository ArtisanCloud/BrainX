"user client";

import DatasetTextList from "@/app/components/space/profile/knowledge/text";

import {
  ActionFetchDatasetListWithConnectedApp,
  Dataset,
  RequestDatasetListWithConnectedApp
} from "@/app/api/knowledge/dataset";
import SelectKnowledgeModal from "@/app/components/space/profile/knowledge/selectKnowledge";
import styles from './index.module.scss';
import {Collapse, Divider} from 'antd';
import {
  ProfileContext,
  ProfileContextType,
} from "@/app/components/space/profile/provider/profile-provider";
import {FormOutlined, PlusOutlined} from '@ant-design/icons';

import {useContext, useEffect, useRef, useState} from "react";
import {ItemType} from 'rc-collapse/es/interface';
import Persona, {RefPersona} from "@/app/components/space/profile/persona";
import {AppContextType, SelectedAppContext} from "@/app/components/space/robot-chat/provider/robot-chat-provider";
import CreateAppProvider from "@/app/components/space/app/provider/create-app-provider";

const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
`;


const ChatProfile = () => {

  const refPerson = useRef<RefPersona>(null);
  const context = useContext(SelectedAppContext) as AppContextType
  const selectedApp = context ? context.selectedApp : null;
  const {showProfile} = useContext(ProfileContext) as ProfileContextType;
  const [needRefreshTextDataset, setNeedRefreshTextDataset] = useState(true)
  const [datasetTextList, setDatasetTextList] = useState<Dataset[]>([]);

  const [containerClassName, setContainerClassName] = useState('');

  const handleEditPersona = () => (
    <FormOutlined
      style={{color: '#aaa', fontSize: '10px'}}
      onClick={(event: any) => {
        // If you don't want click extra trigger collapse, you can prevent this:
        // console.log(refPerson.current);
        if (refPerson.current) {
          refPerson.current.onHandleEdit(); // Call the onEdit method of the child component
          // If you don't want click extra trigger collapse, you can prevent this:
          event.stopPropagation();
        }
      }}
    />
  );

  const openSelectKnowledgeModal = () => (
    <PlusOutlined
      style={{color: '#aaa', fontSize: '10px'}}
      onClick={(event: any) => {
        // If you don't want click extra trigger collapse, you can prevent this:
        setIsSelectKnowledgeModalOpen(true);
        event.stopPropagation();
      }}
    />
  );


  const genExtra = () => (
    <PlusOutlined
      style={{color: '#aaa', fontSize: '10px'}}
      onClick={(event: any) => {
        // If you don't want click extra trigger collapse, you can prevent this:
        event.stopPropagation();
      }}
    />
  );

  type ProfileItem = {
    [key: string]: ItemType[] | undefined;
  }

  const profileItems: ProfileItem = {
    "思考路由": [
      {
        key: 'persona',
        label: '人设和路由',
        children: (
          <CreateAppProvider>
            <Persona ref={refPerson} app={selectedApp!}/>
          </CreateAppProvider>
        ),
        extra: handleEditPersona(),
      },
    ] as ItemType[],

    "技能": [
      {
        key: 'plugin',
        label: '插件',
        children: <div>{text}</div>,
        extra: genExtra(),
      },
      {
        key: 'workflow',
        label: '工作流',
        children: <div>{text}</div>,
        extra: genExtra(),
      }
    ] as ItemType[],

    "知识库": [
      {
        key: 'text',
        label: '文本',
        children: <DatasetTextList datasetTextList={datasetTextList}/>,
        extra: openSelectKnowledgeModal(),
      }
    ] as ItemType[],
    "记忆": [
      {
        key: 'database',
        label: '数据库',
        children: <div>{text}</div>,
        extra: genExtra(),
      },
      {
        key: 'long-term-memory',
        label: '长期记忆',
        children: <div>开启后，会总结对话的内容，在增强机器人对此次对话的理解。</div>,
        extra: genExtra(),
      },
      {
        key: 'variable',
        label: '变量',
        children: <div>{text}</div>,
        extra: genExtra(),
      }
    ] as ItemType[],
    "角色": [
      {
        key: 'voice',
        label: '声音',
        children: <div>{text}</div>,
        extra: genExtra(),
      },
      {
        key: 'hobby',
        label: '兴趣',
        children: <div>{text}</div>,
        extra: genExtra(),
      },
    ] as ItemType[]
  };


  useEffect(() => {
    // 根据 selectedApp 的值设置 containerClassName
    const newClassName = `${styles.container} ${showProfile ? styles.show : styles.hide}`;
    setContainerClassName(newClassName);
    // console.log(containerClassName)
  }, [showProfile]);

  useEffect(() => {
    // 定义一个异步函数来处理数据获取
    const fetchData = async () => {
      // console.log("selectedApp", selectedApp, needRefreshTextDataset)
      if (needRefreshTextDataset && selectedApp) {
        const data = {
          only_connected: true,
          app_uuid: selectedApp?.uuid,
        } as RequestDatasetListWithConnectedApp
        // console.log(data)
        const res = await ActionFetchDatasetListWithConnectedApp(data);
        if (res.data) {
          setDatasetTextList(res.data);
          setNeedRefreshTextDataset(false)
        }
      }
    };

    if (selectedApp && selectedApp.uuid) {
      // 调用该异步函数
      fetchData();

    }

  }, [selectedApp, needRefreshTextDataset]);

  const onChange = (key: string | string[]) => {
    // console.log(key);
  };

  const profileItemKeys = Object.keys(profileItems);
  const [isSelectKnowledgeModalOpen, setIsSelectKnowledgeModalOpen] = useState(false);
  const closeSelectKnowledgeModal = () => {
    setIsSelectKnowledgeModalOpen(false);
  };
  const onRefreshTextDatasetList = () => {
    setNeedRefreshTextDataset(true)
  };


  return (
    <div className={selectedApp?.name == "纯聊天" ? styles.hide : containerClassName}>
      <SelectKnowledgeModal
        appUuid={selectedApp?.uuid!}
        isModalOpen={isSelectKnowledgeModalOpen}
        onClose={closeSelectKnowledgeModal}
        onRefreshTextDatasetList={onRefreshTextDatasetList}
      />
      <div className={styles.list}>
        {profileItemKeys.map((key, index) => (
          <div key={key} className={styles.profileItem}>
            <Divider className={styles.divider} orientation="left">{key}</Divider>
            <Collapse
              style={{
                fontSize: '12px',
                margin: '0',
                padding: '0 !important',
              }}
              key={key}
              defaultActiveKey={['Context']}
              onChange={onChange}
              // variant="borderless"
              expandIconPosition={'start'}
              items={profileItems[key] as ItemType[]}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
export default ChatProfile
