"use client";

import React, { useState, useEffect } from 'react';
import { Modal, Select, Button, Spin } from 'antd';

const { Option } = Select;

interface SelectKnowledgeProps {
  isModalOpen: boolean;
  onClose: () => void;
  onSelect: (knowledgeId: string) => void;
}

const SelectKnowledgeModal: React.FC<SelectKnowledgeProps> = ({ isModalOpen, onClose, onSelect }) => {
  const [knowledgeList, setKnowledgeList] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedKnowledge, setSelectedKnowledge] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isModalOpen) {
      setLoading(true);
      // 模拟数据加载，实际应用中替换为 API 请求
      setTimeout(() => {
        const fetchedData = [
          { id: '1', name: 'Knowledge 1' },
          { id: '2', name: 'Knowledge 2' },
          { id: '3', name: 'Knowledge 3' },
        ];
        setKnowledgeList(fetchedData);
        setLoading(false);
      }, 1000);
    }
  }, [isModalOpen]);

  const handleOk = () => {
    if (selectedKnowledge) {
      onSelect(selectedKnowledge);
      onClose();
    } else {
      alert('Please select a knowledge item');
    }
  };

  const handleCancel = () => {
    onClose();
  };

  return (
    <Modal
      title="Select Knowledge"
      open={isModalOpen}
      onOk={handleOk}
      onCancel={handleCancel}
      footer={null}
      // footer={[
      //   <Button key="back" onClick={handleCancel}>
      //     Cancel
      //   </Button>,
      //   <Button key="submit" type="primary" onClick={handleOk}>
      //     Confirm
      //   </Button>,
      // ]}
    >
      {loading ? (
        <Spin tip="Loading...">
          <div style={{ minHeight: '100px' }} />
        </Spin>
      ) : (
        <Select
          style={{ width: '100%' }}
          placeholder="Choose a knowledge"
          onChange={(value) => setSelectedKnowledge(value)}
        >
          {knowledgeList.map((item) => (
            <Option key={item.id} value={item.id}>
              {item.name}
            </Option>
          ))}
        </Select>
      )}
    </Modal>
  );
};

export default SelectKnowledgeModal
