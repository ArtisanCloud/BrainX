// Droppable.jsx
import React from 'react';
import {useDroppable} from '@dnd-kit/core';

interface DroppableProps {
  onDrop: (event: any) => void; // 可以根据你的事件类型进行更精确的定义
  children: any; // 使用 ReactNode 类型来支持任何类型的子组件
}

const Droppable: React.FC<DroppableProps> = ({onDrop, children}) => {
  const {isOver, setNodeRef} = useDroppable({
    id: 'droppable', // 可以根据需要使用不同的 ID
  });

  const style = {};

  // 当节点被放置时调用 onDrop
  const handleDrop = (event: any) => {
    if (event.over) {
      onDrop(event);
    }
  };

  return (
    <div ref={setNodeRef} style={style} onDrop={handleDrop}>
      {children}
    </div>
  );
}

export default Droppable;
