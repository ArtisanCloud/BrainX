import styles from "./footer.module.scss";

const Footer = () => {
  return (
    <div className={styles.container}>
      <div className={styles.logo}>ArtisanCloud</div>
      <div className={styles.text}>© All rights reserved.</div>
    </div>
  );
};

export default Footer;
