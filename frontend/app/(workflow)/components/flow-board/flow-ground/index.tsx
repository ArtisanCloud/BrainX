import {ReactFlow, Background, Controls} from '@xyflow/react';

const FlowGround = () => {
  return (
    <div style={{height: '100%'}}>
      <ReactFlow>
        <Background/>
        <Controls/>
      </ReactFlow>
    </div>
  )
}

export default FlowGround


