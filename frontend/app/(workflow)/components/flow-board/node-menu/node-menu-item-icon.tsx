import React from 'react';
import styles from './icon.module.scss'; // 请根据实际路径导入样式

const NodeMenuItemIcon = ({ iconInfo }) => {
  const {
    component: IconComponent,
    size = 24,
    backgroundColor = 'transparent'
  } = iconInfo || {};

  return (
    <div className={styles.imgBox}>
      {IconComponent ? (
        <IconComponent
          style={{
            width: `${size}px`,
            height: `${size}px`,
            backgroundColor: backgroundColor,
          }}
          className={styles.nodeItemIcon}
        />
      ) : (
        <div className={styles.nodeItemIcon}>
          <span>?</span>
        </div>
      )}
    </div>
  );
};

export default NodeMenuItemIcon;
