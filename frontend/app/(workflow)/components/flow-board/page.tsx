"use client";

import styles from './index.module.scss';
import {LeftOutlined, PlusOutlined} from '@ant-design/icons';
import {useEffect, useState} from "react";
import {ActionFetchNodeList, NodeTypeInfo} from "@/app/api/workflow/node";
import {iconMapping} from '@/app/(workflow)/components/icon'; // 导入图标映射对象

const FlowBoard = () => {

  const [nodeList, setNodeList] = useState<NodeTypeInfo[]>([])

  useEffect(() => {
    ActionFetchNodeList().then((res) => {
      console.log(res.data)
      setNodeList(res.data)
    })
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.sidebar}>
        <div className={styles.labelBox}>
          <span className={styles.label}>选择节点</span>

          <div className={styles.buttonBox}>
            <button className={styles.hideSidebarButton}>
              <LeftOutlined style={{fontSize: '8px', color: "#6b6b75"}}/>
            </button>

          </div>
        </div>
        {/* 渲染节点列表 */}
        <div className={styles.nodeList}>
          {nodeList.map((node) => {

            // 尝试从 iconMapping 中获取对应的组件
            const iconInfo = iconMapping[node.icon];

            // 如果没有找到，给一个默认的图标组件
            const {component: IconComponent = null, size = 24, backgroundColor = 'transparent'} = iconInfo || {};

            return (
              <div key={node.id} className={styles.nodeContainer}>
                <div className={styles.nodeBox}>
                  <div className={styles.nodeItem}>
                    <div className={styles.imgBox}>
                      {IconComponent ? (
                        <IconComponent
                          style={{
                            width: `${size}px`,
                            height: `${size}px`,
                            backgroundColor: backgroundColor,
                          }}
                          className={styles.nodeIcon}
                        />
                      ) : (
                        <div className={styles.nodeIcon}> {/* 如果没有对应组件，显示默认图标或占位符 */}
                          <span>?</span>
                        </div>
                      )}
                    </div>
                    <span className={styles.nodeName}>{node.name}</span>
                    <button className={styles.addButton}>
                      <PlusOutlined style={{fontSize: '16px', color: "#4d53e8"}}/>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div className={styles.content}></div>
    </div>
  )


}

export default FlowBoard;
