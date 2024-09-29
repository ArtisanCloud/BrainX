import styles from "@/app/(workflow)/workflow/index.module.scss";
import TopBar from "@/app/(workflow)/components/top-bar/page";
import FlowBoard from "@/app/(workflow)/components/flow-board/page";

const WorkflowPage = () => {
  return (
    <div className={styles.container}>
      <TopBar/>
      <FlowBoard/>
    </div>
  );
}

export default WorkflowPage
