"use client";

import {useParams} from "next/navigation";
import React, {useState} from "react";
import {Dataset} from "@/app/api/knowledge/dataset";
import {Document} from "@/app/api/knowledge/document";
import Link from 'next/link'
import styles from "@/app/(workspace)/space/(mine)/knowledge/[uuid]/upload/index.module.scss";
import {Table, Space, Button, Steps, Upload, UploadProps, message, TableProps} from "antd";
import {InboxOutlined, DeleteOutlined} from "@ant-design/icons";
import uiStyles from "@/app/styles/component.module.scss";
import {ActionCreateMediaResource, bucket_name} from "@/app/api/media-resource";

const {Dragger} = Upload;


const UploadLocalDocumentPage = () => {
	const params = useParams<{ uuid: string }>();
	const [currentDataset, setCurrentDataset] = useState<Dataset>();
	const [documents, setDocuments] = useState<Document[]>([]);

	const [current, setCurrent] = useState(0);

	const next = () => {
		setCurrent(current + 1);
	};

	const prev = () => {
		setCurrent(current - 1);
	};

	const stepItems = [
		{
			title: '上传',
		},
		{
			title: '设置分片',
		},
		{
			title: '处理数据',
		},
	]

	const mapStepItems = stepItems.map((item) => ({key: item.title, title: item.title}));

	const uploadDocument = (fileName: string, base64: string, index: number) => {
		console.log(fileName,index)
		// const res = ActionCreateMediaResource({
		// 	mediaName: base64,
		// 	bucketName: bucket_name,
		// 	base64Data: base64,
		// }, index)
	}

	const uploadProps: UploadProps = {
		name: 'files',
		multiple: true,
		beforeUpload(file: any, fileList: any[]) {
			console.log(file, fileList)
			// 检查文件大小是否小于20MB
			const isLt20M = file.size / 1024 / 1024 < 20;
			if (!isLt20M) {
				message.error('files must be smaller than 20MB!');
				return false;
			}

			// 检查总文件数量是否超过3个
			if (fileList.length > 3) {
				message.error('You can only upload up to 3 files!');
				return false;
			}

			const _ = new Promise((resolve) => {
				const reader = new FileReader();
				reader.readAsDataURL(file);
				reader.onload = () => {
					// console.log(reader.result);
					uploadDocument(file.name,reader.result as string, file.index);
				};
			});
		},
	};

	const handleClickDelete = (e:any, document:any) => {
		console.log(e, document)
	}

	interface UploadedDataType {
		key: string;
		documentName: string;
		status: number;
		fileSize: string;
	}

	const uploadedDocumentsTableColumns: TableProps<UploadedDataType>['columns'] = [
		{
			title: '文档名称',
			dataIndex: 'documentName',
			key: 'documentName',
			render: (text) => <a>{text}</a>,
		},
		{
			title: '状态',
			dataIndex: 'status',
			key: 'status',
		},
		{
			title: '文件尺寸',
			dataIndex: 'fileSize',
			key: 'fileSize',
		},
		{
			title: '操作',
			key: 'action',
			dataIndex: 'tags',
			render: (_, document) => (
				<>
					<DeleteOutlined
						onClick={(e) => handleClickDelete(e, document)}  // 包装事件处理函数
						className={uiStyles.btnAction}
					/>
				</>
			),
		}
	];

	const uploadedDocumentsData: UploadedDataType[] = [
		{
			key: '1',
			documentName: 'John Brown',
			status: 1,
			fileSize: '12.23',
		},
	];

	return (

		<div className={styles.container}>
			<div className={styles.path}>
				<div className={styles.pathLink}>
					<Link href={"/space/knowledge/" + currentDataset?.uuid}>
						<span className={styles.back}>&lt;</span>
					</Link>
					<span className={styles.label}>创建新的知识库</span>
				</div>
			</div>
			<div className={styles.main}>
				<div className={styles.stepContainer}>
					<div className={styles.stepView}>
						<Steps current={current} items={mapStepItems}/>

						<div style={{marginTop: 24}}>
							{current < mapStepItems.length - 1 && (
								<div className={styles.stepOneContent}>
									<Dragger
										showUploadList={false}
										maxCount={300}
										{...uploadProps}

									>
										<p className="ant-upload-drag-icon">
											<InboxOutlined/>
										</p>
										<p className="ant-upload-text">点击或者直接拖拽文件上传</p>
										<p className="ant-upload-hint">
											最多300个文件PDF、TXT、DOC、DOCX、MD格式，最多20MB文件，PDF最多支持250页面。
										</p>
									</Dragger>
									{documents.length > 0 ? (
										<div className={styles.uploadedTableContainer}>
											<Table
												columns={uploadedDocumentsTableColumns}
												dataSource={uploadedDocumentsData}
												pagination={{hideOnSinglePage: true}}
											/>
										</div>
									) : null}
									<div className={styles.navContainer}>
										<Button
											disabled={documents.length === 0}
											type="primary"
											onClick={() => next()}
										>
											下一步
										</Button>
									</div>
								</div>
							)}

							{current === stepItems.length - 1 && (
								<Button type="primary" onClick={() => {
								}}>
									Done
								</Button>
							)}
							{current > 0 && (
								<Button style={{margin: '0 8px'}} onClick={() => prev()}>
									Previous
								</Button>
							)}
						</div>
					</div>
				</div>
			</div>
		</div>

	)
		;
}

export default UploadLocalDocumentPage
