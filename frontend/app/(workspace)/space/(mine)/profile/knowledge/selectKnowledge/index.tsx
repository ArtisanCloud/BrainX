"use client";

import React, {useState, useEffect} from 'react';
import {Modal, Select, Button, Spin} from 'antd';

const {Option} = Select;

import styles from './index.module.scss';
import IconText from "@/app/components/icon/knowledge/text";
import {
  ActionDatasetConnectApps, ActionDatasetDisconnectApps,
  ActionFetchDatasetListWithConnectedApp,
  ConnectedDataset, Dataset
} from "@/app/api/knowledge/dataset";
import useLoadingStore from "@/app/store/global-loading";
import {useNotification} from "@/app/components/notification";

interface SelectKnowledgeProps {
  appUuid: string;
  isModalOpen: boolean;
  onClose: () => void;
  onRefreshTextDatasetList: () => void;

}


const SelectKnowledgeModal: React.FC<SelectKnowledgeProps> = (
  {
    appUuid,
    isModalOpen,
    onClose,
    onRefreshTextDatasetList,
  }
) => {
  const [datasetList, setDatasetList] = useState<ConnectedDataset[]>([]);
  const {loading, setLoading} = useLoadingStore()
  const {msgSuccess, msgWarn, msgError} = useNotification();

  useEffect(() => {
    // 定义一个异步函数来处理数据获取
    const fetchData = async () => {
      if (isModalOpen) {
        const res = await ActionFetchDatasetListWithConnectedApp({
          only_connected: false,
          app_uuid: appUuid
        });
        if (res.data) {
          setDatasetList(res.data);
        }
      }
    };

    // 调用该异步函数
    fetchData();
  }, [appUuid, isModalOpen]);

  const handleOk = () => {
    // if (selectedKnowledge) {
    //   onSelect(selectedKnowledge);
    //   onClose();
    // } else {
    //   alert('Please select a knowledge item');
    // }
  };

  const handleCancel = () => {
    onClose();
  };

  const handleConnectDataset = async (dataset: Dataset) => {
    // console.log(dataset)
    try {
      setLoading(true)
      const res = await ActionDatasetConnectApps({
        app_uuid: appUuid,
        dataset_uuids: [dataset.uuid!],
      })
      if (res.result) {
        setDatasetList(prevList =>
          prevList.map(item =>
            item.uuid === dataset.uuid ? {...item, with_app_connected: true} : item
          )
        );

        // 调用外部事件通知
        onRefreshTextDatasetList(); // 通知外部使用了知识库

      }

      msgSuccess("使用知识库成功")
    } catch (e: any) {
      msgError("使用知识库失败")
    } finally {
      setLoading(false)
    }
  }

  const handleDisconnectDataset = async (dataset: Dataset) => {
    // console.log(dataset)
    try {
      setLoading(true)
      const res = await ActionDatasetDisconnectApps({
        app_uuid: appUuid,
        dataset_uuids: [dataset.uuid!],
      })
      if (res.result) {
        setDatasetList(prevList =>
          prevList.map(item =>
            item.uuid === dataset.uuid ? {...item, with_app_connected: false} : item
          )
        );
        // 调用外部事件通知
        onRefreshTextDatasetList(); // 通知外部使用了知识库
      }

      msgSuccess("取消知识库成功")
    } catch (e: any) {
      msgError("取消知识库失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal
      title="选择知识库"
      open={isModalOpen}
      onOk={handleOk}
      onCancel={handleCancel}
      footer={null}
      width={1000}
      // footer={[
      //   <Button key="back" onClick={handleCancel}>
      //     Cancel
      //   </Button>,
      //   <Button key="submit" type="primary" onClick={handleOk}>
      //     Confirm
      //   </Button>,
      // ]}
    >

      <div className={styles.container}>
        <div className={styles.header}>
          <div className={styles.tab}>
            <div className={styles.tabItem}>全部</div>
            <div className={styles.tabDivider}></div>
            <div className={styles.tabItem}>文档</div>
            <div className={styles.tabDivider}></div>
            <div className={styles.tabItem}>表格</div>
            <div className={styles.tabDivider}></div>
            <div className={styles.tabItem}>照片</div>
          </div>
          <div className={styles.rightSlot}>
            <div className={styles.combobox}>
              <Select style={{width: 160}}>
                <Option>创建时间</Option>
                <Option>编辑时间</Option>
              </Select>
            </div>
            <div className={styles.searchBox}>
              <div>Search</div>
            </div>

            <Button className={styles.buttonCreateKnowledge}>创建知识库</Button>

          </div>
        </div>
        <div className={styles.content}>
          {
            datasetList.map((item) => (
                <div key={item.uuid} className={styles.item}>
                  <div className={styles.avatar}>
                    <IconText width={36} height={36}/>
                  </div>
                  <div className={styles.itemContent}>
                    <span className={styles.title}>{item.name}</span>
                    <span className={styles.description}>{item.description}</span>
                    <div className={styles.tagWrapper}>
                      <div className={styles.tags}>
                        <div className={styles.tag}>
                          <div className={styles.tagContent}>6.27 MB</div>
                        </div>
                        <div className={styles.tag}>
                          <div className={styles.tagContent}>3个</div>
                        </div>
                      </div>
                      <span className={styles.info}>创建时间 {item.createdAt}</span>
                    </div>
                  </div>
                  <div className={styles.right}>
                    {
                      !item.with_app_connected
                        ?
                        <Button onClick={() => handleConnectDataset(item)} className={styles.addButton}>添加</Button>
                        :
                        <Button onClick={() => handleDisconnectDataset(item)}
                                className={styles.removeButton}>移除</Button>
                    }
                  </div>
                </div>
              )
            )}
        </div>
      </div>

    </Modal>
  );
};

export default SelectKnowledgeModal
