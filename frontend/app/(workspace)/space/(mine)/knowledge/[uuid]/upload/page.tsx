"use client";

import {useParams} from "next/navigation";
import React, {useEffect, useState} from "react";
import {Dataset, SegmentationMode} from "@/app/api/knowledge/dataset";
import Link from 'next/link'
import styles from "@/app/(workspace)/space/(mine)/knowledge/[uuid]/upload/index.module.scss";
import {
	Table,
	Button,
	Steps,
	Upload,
	UploadProps,
	message,
	TableProps,
	Space,
	Radio,
	Select,
	Input,
	Checkbox
} from "antd";
import {
	InboxOutlined,
	DeleteOutlined,
	FilePdfOutlined,
	FileWordOutlined,
	FileTextOutlined,
	FileImageOutlined,
	FileUnknownOutlined,
	CheckCircleOutlined,
	CloseCircleOutlined
} from '@ant-design/icons';
import {AllowedFileTypes, segmentationOptions} from "@/app/utils/dataset";

import uiStyles from "@/app/styles/component.module.scss";
import {ActionCreateMediaResource, bucket_name, MediaResource} from "@/app/api/media-resource";
import {ContentType} from "@/app/utils/media";

const {Dragger} = Upload;


const UploadLocalDocumentPage = () => {
	const params = useParams<{ uuid: string }>();
	const [currentDataset, setCurrentDataset] = useState<Dataset>();
	const [documents, setDocuments] = useState<MediaResource[]>([]);

	const [current, setCurrent] = useState(0);
	const [segmentMode, setSegmentMode] = useState<SegmentationMode>(SegmentationMode.AUTOMATIC);
	const [selectedSegmentID, setSelectedSegmentID] = useState('\n');
	const [segmentMaxLength, setSegmentMaxLength] = useState(800);
	const [replaceConsecutiveSpaces, setReplaceConsecutiveSpaces] = useState(false);
	const [deleteAllUrls, setDeleteAllUrls] = useState(false);


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

	const uploadDocument = async (fileName: string, base64: string, index: number) => {
		// console.log(fileName, index)
		const res = await ActionCreateMediaResource({
			mediaName: fileName,
			bucketName: bucket_name,
			base64Data: base64,
			sortIndex: index,
		})
		if (res.media_resource.url) {
			setDocuments((prevDocuments) => [
				...prevDocuments,
				res.media_resource
			]);
		}

	}

	const uploadProps: UploadProps = {
		name: 'files',
		multiple: true,
		beforeUpload(file: any, fileList: any[]) {
			// console.log(file, fileList)

			// 检查文件大小是否小于20MB
			const isLt20M = file.size / 1024 / 1024 < 20;
			if (!isLt20M) {
				message.error('files must be smaller than 20MB!');
				return false;
			}


			// 修正条件判断，检查文件类型是否在允许的范围内
			if (!AllowedFileTypes.includes(file.type)) {

				message.error(`${file.name} is not a PDF, TXT, DOC, DOCX, or MD file`);
				return false;
			}

			// 检查总文件数量是否超过最大数
			if (fileList.length > 300) {
				message.error('You can only upload up to 300 files!');
				return false;
			}

			// console.log(file.uid);
			// 使用 split 将字符串分割成数组
			const parts = file.uid.split('-');
			// 获取最后一个部分
			const lastPart = parts[parts.length - 1];
			// console.log(lastPart);
			// 将最后一个部分转换为整数
			let sortIndex = parseInt(lastPart, 10);
			// console.log(sortIndex);

			const reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = () => {
				// console.log(reader.result);
				const _ = uploadDocument(file.name, reader.result as string, sortIndex);
			};

			return false;
		},
	};

	// useEffect(() => {
	// 	console.log(current, stepItems.length)
	// }, [current])

	const handleDeleteDocument = (e: any, document: any) => {
		// console.log(e, document)
		e.stopPropagation(); // 阻止事件冒泡，如果需要的话

		setDocuments((prevDocuments) =>
			prevDocuments.filter((doc) => doc.id !== document.id)
		);
	}

	const handleChangeSelectedSegmentID = (value) => {
		setSelectedSegmentID(value);
	};

	const handleChangeSegmentMaxLength = (value) => {
		setSegmentMaxLength(value);
	};


	const getFileIcon = (contentType: string) => {
		// console.log(contentType)
		switch (contentType) {
			case ContentType.PDF:
				return <FilePdfOutlined/>;
			case ContentType.DOC:
			case ContentType.DOCX:
				return <FileWordOutlined/>;
			case ContentType.TXT:
				return <FileTextOutlined/>;
			case ContentType.PNG:
			case ContentType.JPEG:
			case ContentType.GIF:
				return <FileImageOutlined/>;
			default:
				return <FileUnknownOutlined/>;
		}
	};

	const uploadedDocumentsTableColumns: TableProps<MediaResource>['columns'] = [
		{
			title: '文档名称',
			dataIndex: 'filename',
			key: 'filename',
			render: (filename: string, record: any) => (
				<>
					{getFileIcon(record.content_type)}
					<span style={{marginLeft: "20px"}}>{filename}</span>
				</>
			),
		},
		{
			title: '状态',
			key: 'status',
			render: (_, record: any) => (
				<>
					{record.deletedAt == null ? (
						<>
							<CheckCircleOutlined style={{color: 'green'}}/><span className={'ml-2'}>已上传</span>
						</>
					) : (
						<>
							<CloseCircleOutlined style={{color: 'red'}}/><span className={'ml-2'}>失败</span>
						</>
					)}
				</>
			)
		},
		{
			title: '文件尺寸',
			dataIndex: 'size',
			key: 'fileSize',
			render: (size: number) => `${(size / 1024).toFixed(2)} KB`,  // 转换为 KB 并保留两位小数
		},
		{
			title: '操作',
			key: 'action',
			dataIndex: 'tags',
			render: (_, record) => (
				<>
					<DeleteOutlined
						onClick={(e) => handleDeleteDocument(e, record)}  // 包装事件处理函数
						className={uiStyles.btnAction}
					/>
				</>
			),
		}
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
							{current <= mapStepItems.length - 3 && (
								<div className={styles.stepOneContent}>
									<Dragger
										showUploadList={false}
										maxCount={300}
										accept={AllowedFileTypes}
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
												dataSource={documents.map((doc) => ({...doc, key: doc.id}))} // 添加唯一的 key
												pagination={{hideOnSinglePage: true}}
											/>
										</div>
									) : null}
									<div className={styles.navContainer}>
										<Button
											// disabled={documents.length === 0}
											type="primary"
											onClick={() => next()}
										>
											下一步
										</Button>
									</div>
								</div>
							)}

							{current === stepItems.length - 2 && (
								<div className={styles.stepTwoContent}>
									<div className={styles.selectSegmentModeContainer}>
										<Radio.Group value={segmentMode}>
											<Space className={styles.radioGroup} direction="vertical">
												<div
													className={`${styles.automatic} ${segmentMode === SegmentationMode.AUTOMATIC ? styles['automatic-mode'] : styles['other-mode']}`}
													onClick={() => setSegmentMode(SegmentationMode.AUTOMATIC)}
												>
													<div className={styles.radio}>
														<Radio value={SegmentationMode.AUTOMATIC}></Radio>
													</div>
													<div className={styles.automaticDescription}>
														<span className={styles.title}>自动分片 & 清洗</span>
														<div className={styles.description}>自动分片 & 预处理规则</div>
													</div>
												</div>
												<div
													className={`${styles.custom} ${segmentMode === SegmentationMode.CUSTOM ? styles['custom-mode'] : styles['other-mode']}`}
													onClick={() => setSegmentMode(SegmentationMode.CUSTOM)}
												>
													<div className={styles.radio}>
														<Radio value={SegmentationMode.CUSTOM}></Radio>
													</div>
													<div className={styles.customDescription}>
														<span className={styles.title}>自定义</span>
														<div className={styles.description}>自定义分片规则 & 分片长度 & 处理规则</div>
														{segmentMode === SegmentationMode.CUSTOM && (
															<div className={styles.customConfig}>
																<div className={styles.separate}></div>
																<div className={styles.segmentField}>
																	<span className={styles.title}>分段识别符号</span>
																	<Select
																		className={styles.select}
																		options={segmentationOptions}
																		value={selectedSegmentID}
																		onChange={handleChangeSelectedSegmentID}
																		placeholder="请选择一个识别符号"
																		style={{width: '100%'}}
																	/>
																</div>
																<div className={styles.segmentField}>
																	<span className={styles.title}>最大切分长度</span>
																	<Input onChange={handleChangeSegmentMaxLength}
																				 className={styles.input}
																				 value={800}
																	/>
																</div>
																<div className={styles.segmentField}>
																	<span className={styles.title}>文本预处理规则</span>
																	<Checkbox className={styles.checkbox}
																						onChange={(e)=>setDeleteAllUrls(e.target.value)}
																	>将连续的空格、换行符和制表符替换掉
																	</Checkbox>
																	<Checkbox className={styles.checkbox}
																						onChange={(e)=>setDeleteAllUrls(e.target.value)}
																	>删除所有的URL和电子邮件地址
																	</Checkbox>
																</div>
															</div>
														)}
													</div>
												</div>
											</Space>
										</Radio.Group>
									</div>
									<div className={styles.navContainer}>
										<Button style={{margin: '0 8px'}} onClick={() => prev()}>
											上一步
										</Button>
										<Button type="primary" onClick={() => next()}>
											下一步
										</Button>
									</div>
								</div>
							)}
							{current >= stepItems.length - 1 && (

								<Button style={{margin: '0 8px'}} onClick={() => prev()}>
									Done
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
