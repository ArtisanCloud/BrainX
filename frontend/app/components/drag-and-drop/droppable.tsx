// Droppable.jsx
import React from 'react';
import { useDroppable } from '@dnd-kit/core';

function Droppable({ onDrop, children }) {
  const { isOver, setNodeRef } = useDroppable({
    id: 'droppable', // 可以根据需要使用不同的 ID
  });

  const style = {
  };

  // 当节点被放置时调用 onDrop
  const handleDrop = (event) => {
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
