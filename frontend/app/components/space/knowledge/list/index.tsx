"use client";

import styles from './index.module.scss';
import uiStyles from '@/app/styles/component.module.scss';
import React, {useContext, useEffect, useState} from "react";
import {Table, Space, TableProps, Switch, Dropdown, MenuProps} from "antd";
import {MoreOutlined, BlockOutlined, DeleteOutlined} from "@ant-design/icons";
import {
  FetchDatasetListContext,
  FetchDatasetListContextType
} from "@/app/components/space/knowledge/provider/fetch-dataset-list-provider";
import {defaultPage, pageSize} from "@/app/config/constant";
import {Dataset, ResponseFetchDatasetList} from "@/app/api/knowledge/dataset";
import Image from "next/image";
import {GetOssUrl} from "@/app/lib/url";
import {getDatasetImportTypeTranslation} from "@/app/utils/dataset"
import {EditIcon} from "@nextui-org/shared-icons";
import moment from "moment";
import {useRouter} from "next/navigation";


const DatasetList = () => {
  const router = useRouter();

  const [currentDataset, setCurrentDataset] = useState<Dataset>();

  const {
    datasetList, setDatasetList,
    fetchDatasetList,
    pagination, setPagination
  } = useContext(FetchDatasetListContext) as FetchDatasetListContextType;


  useEffect(() => {
    // console.log(pagination)
    let _page = pagination?.page ?? defaultPage
    let _pageSize = pagination?.per_page ?? pageSize

    fetchDatasetList({
      page: _page,
      page_size: _pageSize,
    }).then((res: ResponseFetchDatasetList) => {
      // console.log(res)
      setDatasetList(res.data)
      setPagination(res.pagination)
    })

  }, [pagination?.page, pagination?.per_page]); // 添加缺失的依赖项

  const onChange = (page: number, pageSize: number) => {
    // console.log("onChange", page, pageSize)
    setPagination({
      ...pagination,
      page: page,
    })

  }


  const handleEdit = (record: Dataset) => {
    // console.log("edit",record)
  }

  const handleDelete = (record: Dataset) => {
    // console.log("delete",record)
  }


  const handleClickDataset = (e: any, record: Dataset) => {
    // console.info('Click on action button.', record);
    e.stopPropagation()
    setCurrentDataset(record)

  };

  const handleClickAction: MenuProps['onClick'] = (e) => {

    if (e.key == 'edit') {
      handleEdit(currentDataset!)
    } else if (e.key == 'delete') {
      handleDelete(currentDataset!)
    }

  };


  const items: MenuProps['items'] = [
    {
      label: '编辑',
      key: 'edit',
      icon: <EditIcon/>,
    },
    {
      label: '删除',
      key: 'delete',
      icon: <DeleteOutlined/>,
      danger: true,
    },
  ]

  const menuProps = {
    items,
    onClick: handleClickAction,
  };

  const columns: TableProps<Dataset>['columns'] = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (_, dataset: Dataset) =>
        <div className={'flex flex-row'}>
          {dataset.avatar_url ? (<Image
              priority
              width={68}
              height={68}
              alt={'app avatar'}
              className={'rounded-lg border-1'}
              src={GetOssUrl(dataset.avatar_url)}/>
          ) : (
            <div className={'w-16 h-16 flex'}>
              <BlockOutlined
                style={{fontSize: '32px', color: 'white', backgroundColor: '#5295e5'}}
                className="place-content-center rounded-lg border-1 w-full h-full"
              />
            </div>

          )}
          <div className={'flex flex-col justify-center ml-3 border-0'}>
            <span className={'border-0'} style={{fontWeight: 'bold'}}>{dataset.name}</span>
            <span style={{fontSize: '12px', color: 'gray'}}>{dataset.description}</span>
          </div>
        </div>
    },
    {
      title: '类型',
      key: 'type',
      render: (_, record) => (
        <Space size="middle">
          {getDatasetImportTypeTranslation(record?.import_type!)}
        </Space>
      ),
    },
    {
      title: '尺寸',
      dataIndex: 'word_count',
      key: 'word_count',
      render: (text, record) => (
        record.word_count !== null ? record.word_count : 0
      ),
    },
    {
      title: '结束时间',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
      render: (_, record) => (
        record.updatedAt ? moment(record.updatedAt).format('YYYY-MM-DD HH:mm:ss') : ''
      ),
    },
    {
      title: '启动',
      key: 'is_published',
      render: (_, record) => (
        <Space size="middle">
          <Switch
            onClick={(value, e) => handleClickEnable(e, value, record)}
            checkedChildren="开启"
            unCheckedChildren="关闭"
            checked={record.is_published}
          />
        </Space>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Dropdown
            menu={menuProps}
            placement="bottom"
            arrow={{pointAtCenter: true}}
            trigger={['click']}
          >
            <MoreOutlined
              onClick={(e) => handleClickDataset(e, record)}  // 包装事件处理函数
              className={uiStyles.btnAction}
            />
          </Dropdown>

        </Space>
      ),
    },
  ];

  const handleClickEnable = (e: any, value: boolean, dataset: Dataset) => {
    e.stopPropagation();
    console.log(value, dataset)

  }

  const onSelectRow = (dataset: Dataset) => {
    // console.log('selectedRowKeys changed: ', dataset);
    router.push('knowledge/' + dataset.uuid)
  };


  return (
    <div className={styles.container}>
      <Table columns={columns}
             dataSource={datasetList}
             rowKey="uuid"
             onRow={(record) => ({
               onClick: () => onSelectRow(record),
             })}
      />
    </div>
  );
}

export default DatasetList;
