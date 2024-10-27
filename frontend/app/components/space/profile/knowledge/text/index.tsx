import styles from './index.module.scss';
import { Dataset } from "@/app/api/knowledge/dataset";

interface TextKnowledgeListProps {
  textKnowledge?: Dataset[];
}

const TextKnowledgeList: React.FC<TextKnowledgeListProps> = ({ textKnowledge = [] }) => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        {textKnowledge.length > 0 ? (
          textKnowledge.map((item, index) => (
            <div key={index} className="grid grid-flow-row gap-y-[4px]">{item.name}</div>
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

export default TextKnowledgeList;
