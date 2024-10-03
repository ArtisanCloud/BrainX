// app/DragAndDropPage.jsx

"use client";

import { useState } from 'react';
import {
  DndContext,
  useDroppable,
  useDraggable,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
} from '@dnd-kit/sortable';

// 初始项目
const initialItems = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];

// 可排序项组件
const SortableItem = ({ id }) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useDraggable({
    id,
  });

  // 确保 transition 是字符串
  const style: React.CSSProperties = {
    transform: transform ? `translate3d(${transform.x}px, ${transform.y}px, 0)` : undefined,
    transition: transition ? `${transition}` : undefined, // 确保 transition 是字符串
    border: '1px solid lightgray',
    padding: '8px',
    margin: '4px 0',
    backgroundColor: 'white',
    cursor: 'grab',
    userSelect: 'none',
  };

  return (
    <li ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {id}
    </li>
  );
};

// 可放置区域组件
const DroppableArea = ({ id, title, children }) => {
  const { setNodeRef } = useDroppable({ id });

  return (
    <div
      ref={setNodeRef}
      style={{
        width: '200px',
        height: '300px',
        border: '2px dashed lightgray',
        padding: '10px',
        margin: '0 20px',
        backgroundColor: '#f9f9f9',
      }}
    >
      <h3>{title}</h3>
      {children}
    </div>
  );
};

// 主组件
export default function DragAndDropPage() {
  const [leftItems, setLeftItems] = useState(initialItems);
  const [rightItems, setRightItems] = useState([]);

  const handleDragEnd = (event) => {
    const { active, over } = event;

    // 拖动到右边区域
    if (over?.id === 'droppable-right') {
      setRightItems((items) => [...items, active.id]);
      setLeftItems((items) => items.filter((item) => item !== active.id));
    }

    // 拖动到左边区域
    if (over?.id === 'droppable-left') {
      setLeftItems((items) => [...items, active.id]);
      setRightItems((items) => items.filter((item) => item !== active.id));
    }
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '20px' }}>
        {/* 左边区域 */}
        <DroppableArea id="droppable-left" title="Left Area">
          <SortableContext items={leftItems}>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {leftItems.map((item) => (
                <SortableItem key={item} id={item} />
              ))}
            </ul>
          </SortableContext>
        </DroppableArea>

        {/* 右边区域 */}
        <DroppableArea id="droppable-right" title="Right Area">
          <SortableContext items={rightItems}>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {rightItems.map((item) => (
                <SortableItem key={item} id={item} />
              ))}
            </ul>
          </SortableContext>
        </DroppableArea>
      </div>
    </DndContext>
  );
}
