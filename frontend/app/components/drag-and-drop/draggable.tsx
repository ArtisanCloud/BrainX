import React from 'react';
import {useDraggable} from '@dnd-kit/core';
import ReactDOM from 'react-dom';

function Draggable(props: any) {
  const {attributes, listeners, setNodeRef, transform, isDragging} = useDraggable({
    id: props.id,
  });

  // 拖动元素的样式
  const dragStyle: React.CSSProperties = {
    transform: transform ? `translate3d(${transform.x}px, ${transform.y}px, 0)` : 'none', // 拖动时的位置
    zIndex: 9999,
    position: 'relative', // 使用绝对定位
    opacity: isDragging ? 0.5 : 1, // 拖动时降低透明度
  };

  // 原地元素的样式
  const staticStyle: React.CSSProperties = {
    position: 'absolute',
    top: props.nodeTop,
    opacity: isDragging ? 1 : 0, // 拖动时原地元素隐身
  };

  const dragElement = (
    <div style={staticStyle}>
      {props.children}
    </div>
  );

  return (
    <>
      {/* 自动拖拽的元素 */}
      <div ref={setNodeRef} style={dragStyle} {...listeners} {...attributes}>
        {props.children}
      </div>
      {/* 拖拽时，显示原地的元素 */}
      {isDragging && props.containerRef && ReactDOM.createPortal(dragElement, props.containerRef)}
    </>
  );
}

export default Draggable;
