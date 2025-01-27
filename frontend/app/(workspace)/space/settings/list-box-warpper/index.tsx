import styles from './index.module.scss';
import { ReactNode } from 'react';


interface ListBoxWrapperProps {
  children: ReactNode; // 显式声明 children 的类型
}

export const ListBoxWrapper = ({ children }: ListBoxWrapperProps) => (
  
  <div className={styles.listBoxWrapper}>
    {children}
  </div>
);
