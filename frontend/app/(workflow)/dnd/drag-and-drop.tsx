import React, { CSSProperties, useState } from 'react';
import { DndContext, useDraggable, useDroppable } from '@dnd-kit/core';
import styles from './index.module.scss';

interface DraggableItemProps {
  id: string;
  children: React.ReactNode; // 使用 ReactNode 替代 any，确保更严格的类型检查
  isDragging: boolean;
}

const DraggableItem: React.FC<DraggableItemProps> = ({ id, children, isDragging }) => {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id,
    data: { label: children }, // 仍然可以保留 label 信息
  });

  const draggingStyle: CSSProperties = {
    transform: transform ? `translate3d(${transform.x}px, ${transform.y}px, 0)` : 'none',
    position: 'absolute',
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      {...listeners}
      {...attributes}
      className={styles.draggableItem}
      style={isDragging ? draggingStyle : {}}
    >
      {children}
    </div>
  );
};

interface DroppableAreaProps {
  onDrop?: (event: any) => void; // 使用 any 以便灵活处理 DnD 事件，具体类型可根据需要进一步定义
}

const DroppableArea: React.FC<DroppableAreaProps> = ({ onDrop }) => {
  const { isOver, setNodeRef } = useDroppable({
    id: 'droppable',
  });

  return (
    <div
      ref={setNodeRef}
      className={`${styles.dropZone} ${isOver ? styles.dropZoneActive : ''}`}
      onDrop={onDrop}
    >
      <h3>Drop here</h3>
    </div>
  );
};

interface DroppedItem {
  id: string;
  label: string;
}

const DragAndDropDemo: React.FC = () => {
  const [items] = useState<{ id: string; label: string }[]>([
    { id: '1', label: 'Item 1' },
    { id: '2', label: 'Item 2' },
    { id: '3', label: 'Item 3' },
  ]);
  const [droppedItems, setDroppedItems] = useState<DroppedItem[]>([]);
  const [draggingItemId, setDraggingItemId] = useState<string | null>(null); // 允许为 null

  const handleDragStart = (event: any) => {
    setDraggingItemId(event.active.id);
  };

  const handleDrop = (event: any) => {
    const { active } = event;
    if (active) {
      const label = active.data.current.label || 'Unnamed Item';
      if (!droppedItems.some((item) => item.id === active.id)) {
        setDroppedItems((prev) => [...prev, { id: active.id, label }]);
      }
    }
    setDraggingItemId(null);
  };

  return (
    <DndContext onDragEnd={handleDrop} onDragStart={handleDragStart}>
      <div className={styles.container}>
        <div className={styles.sidebar}>
          <h3>Drag from here</h3>
          {items.map((item) => (
            <div key={item.id} style={{ position: 'relative' }}>
              <DraggableItem id={item.id} isDragging={draggingItemId === item.id}>
                {item.label}
              </DraggableItem>
              {draggingItemId === item.id && (
                <div className={`${styles.draggableItem} ${styles.placeholder}`}>
                  {item.label}
                </div>
              )}
            </div>
          ))}
        </div>
        <DroppableArea onDrop={handleDrop} />
        <div className={styles.droppedItems}>
          <h3>Dropped Items</h3>
          {droppedItems.map((item) => (
            <div key={item.id} className={styles.droppedItem}>
              {item.label}
            </div>
          ))}
        </div>
      </div>
    </DndContext>
  );
};

export default DragAndDropDemo;
