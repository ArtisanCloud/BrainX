import styles from './index.module.scss';
import {Dataset} from "@/app/api/knowledge/dataset";
import IconText from "@/app/components/icon/knowledge/text";
import {CopyOutlined, MinusCircleOutlined} from '@ant-design/icons';
import {Button} from 'antd';

interface DatasetTextListProps {
  datasetTextList?: Dataset[];
}

const DatasetTextList: React.FC<DatasetTextListProps> = ({datasetTextList = []}) => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        {datasetTextList.length > 0 ? (
          datasetTextList.map((item, index) => (
            <div key={index} className={styles.item}>
              <div className={styles.itemContent}>
                <div className={styles.avatar}>
                  <IconText width={36} height={36} fontSize={12}/>
                </div>
                <div className={styles.itemInfo}>
                  <div className={styles.title}>{item.name}</div>
                  <div className={styles.description}>{item.description}</div>
                </div>
                <div className={styles.right}>
                  <Button className={styles.button} icon={<CopyOutlined/>}/>
                  <Button className={styles.button} icon={<MinusCircleOutlined/>}/>
                </div>
              </div>

            </div>
          ))
        ) : (
          <div className="text-center text-gray-500">
            暂无关联知识库文本，可以到知识库中创建
          </div>
        )}
      </div>
    </div>
  );
}

export default DatasetTextList;
