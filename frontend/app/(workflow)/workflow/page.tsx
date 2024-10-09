import styles from "@/app/(workflow)/workflow/index.module.scss";
import TopBar from "@/app/(workflow)/components/top-bar/index";
import FlowBoard from "@/app/(workflow)/components/flow-board/index";

const WorkflowPage = () => {
  return (
    <div className={styles.container}>
      <TopBar/>
      <FlowBoard/>
    </div>
  );
}

export default WorkflowPage
