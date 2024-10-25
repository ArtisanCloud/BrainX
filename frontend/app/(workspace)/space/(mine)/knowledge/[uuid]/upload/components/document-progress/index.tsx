import React, {useEffect, useState} from 'react';
import styles from './index.module.scss'; // 确保引入你的样式文件
import {Document} from '@/app/api/knowledge/document';
import {FilePdfOutlined} from '@ant-design/icons';
import {ActionQueryTasksStatus, ActionRunMultiple30SecondsTasks, ResponseQueryTasksStatus} from "@/app/api/task";

const DocumentProgress = (
  {documents, taskUuids}: { documents: Document[], taskUuids: string[] }
) => {

  const [progressStatus, setProgressStatus] = useState<number[]>([]);
  const [allCompleted, setAllCompleted] = useState(false)
  // 函数用于计算字数
  // 估算文件大小（MB）根据字数
  const estimateFileSize = (wordCount: number) => {
    if (wordCount <= 0) return 0; // 处理字数为0的情况

    // 假设每个字占用2字节（对于中文）或1字节（对于英文）
    const byteCount = wordCount * 2; // 假设平均每个字占用2字节
    // 将字节转换为MB，1MB = 1024 * 1024 字节
    const sizeInMB = (byteCount / (1024 * 1024)).toFixed(2); // 保留两位小数

    return sizeInMB; // 返回文件大小
  };

  useEffect(() => {
    const intervalId = setInterval(async () => {
      const res: ResponseQueryTasksStatus = await ActionQueryTasksStatus({
        task_uuids: taskUuids,
      });

      if (res) {
        const newProgressStatus: number[] = [];
        Object.keys(res).forEach((taskId, index) => {
          const taskStatus = res[taskId];
          // console.log(taskStatus)
          if (taskStatus.state == "SUCCESS") {
            newProgressStatus[index] = 100;  // 任务完成，进度为 1
          } else if (taskStatus.state == "STARTED") {
            newProgressStatus[index] = taskStatus.current / taskStatus.total * 100;  // 获取当前进度，默认值为 0
          } else {
            newProgressStatus[index] = 0
          }
        });

        setProgressStatus(newProgressStatus);


        // 检查所有任务的当前进度是否为总进度（完成状态）
        const allCompleted = newProgressStatus.every(status => status === 1);


        if (allCompleted) {
          setAllCompleted(true)
          clearInterval(intervalId); // 停止轮询
        }
      }
    }, 5000); // 每5秒更新一次

    return () => clearInterval(intervalId); // 组件卸载时清除定时器
  }, [taskUuids]);

  useEffect(() => {
    console.log('Updated statusMap:', progressStatus);
  }, [progressStatus]);

  return (
    <div className={styles.container}>
      <div className={styles.progressStatusLabel}>
        {allCompleted ? "服务器处理完上传文件" : "服务器处理中，可以点击关闭窗口，后台会继续执行任务"}
      </div>

      {documents.map((document, index) => {
        // 计算当前文档的字数
        const wordCount = estimateFileSize(document.word_count!); // 假设 content 是一个字符串


        return (
          <div key={document.uuid || index}
               className={styles.progressWrapper}
               style={{"--progress": `${progressStatus[index]}%`} as React.CSSProperties}
          >
            <div className={styles.content}>
              <div className={styles.info}>
                <span className={styles.preview}>
                  <FilePdfOutlined/>
                </span>
                <div className={styles.fileInfo}>
                  <div className={styles.title}>{document.title}</div>
                  <div className={styles.fileSize}>
                    {wordCount} MB {/* 在这里显示计算后的 word_count */}
                  </div>
                </div>
              </div>
            </div>
            <div className={styles.right}>处理完成</div>
          </div>
        );
      })}
    </div>
  );
}

export default DocumentProgress;
