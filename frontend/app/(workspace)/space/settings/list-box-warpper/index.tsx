import styles from './index.module.scss';

export const ListBoxWrapper = ({  children }) => (
  <div className={styles.listBoxWrapper}>
    {children}
  </div>
);
