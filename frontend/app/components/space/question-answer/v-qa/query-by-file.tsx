"use client";

import styles from './index.module.scss';
import {Form, Upload, FormProps, UploadProps, Input, Image, Divider, Button, Typography} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import React, {Fragment, useContext, useState} from "react";
import {ActionVisualQueryByFile, RequestVisualQuery} from "@/app/api/question-answer/visual-query";
import useCountdown from "@/app/lib/countdown";
import {SelectLLMContext, SelectLLMContextType} from "@/app/components/space/provider/llm";

const {Dragger} = Upload;
const {TextArea} = Input;

const VisualQuestionAnswerByFile = () => {
	const [targetImage, setTargetImage] = useState<string>('');
	const [uploadFile, setUploadFile] = useState<File | null>(null);
	const [answer, setAnswer] = useState('');
	const {countdown, startCountdown, stopCountdown} = useCountdown(0);
	const {selectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;

	const secondsCountDown = 60;

	const props: UploadProps = {
		multiple: false,
		beforeUpload(file: File) {
			return new Promise((resolve) => {
				const reader = new FileReader();
				reader.readAsDataURL(file);
				reader.onload = () => {
					setTargetImage(reader.result as string);
					setUploadFile(file);
				};
			});
		},
	};

	const onFinish: FormProps<RequestVisualQuery>["onFinish"] = async (values: RequestVisualQuery) => {
		if (!uploadFile) {
			console.error("No file uploaded");
			return;
		}

		values.llm = selectedLlm!;
		
		try {
			startCountdown(secondsCountDown);
			setAnswer('');
			const res = await ActionVisualQueryByFile(values, uploadFile);
			setAnswer(res.answer);
		} catch (error) {
			console.error("请求失败:", error);
		} finally {
			stopCountdown();
		}
	};

	const onFinishFailed: FormProps<RequestVisualQuery>["onFinishFailed"] = (errorInfo: any) => {
		console.log('Failed:', errorInfo);
	};

	const clearUpload = () => {
		setTargetImage('');
		setUploadFile(null);
		setAnswer('');
	};

	return (
		<div className={styles.container}>
			<div className={styles.queryImage}>
				<div className={`${styles.imageDragger} ${targetImage === '' ? '' : styles.hide}`}>
					<Dragger {...props}>
						<p className="ant-upload-drag-icon">
							<InboxOutlined/>
						</p>
						<p className="ant-upload-text">点击或者拖拽图片文件到这个区域</p>
						<p className="ant-upload-hint">
							当前只支持单张图片，请不要文件过大。
						</p>
					</Dragger>
				</div>
				<div className={`${styles.preview} ${targetImage == '' ? styles.hide : ''}`}>
					<Image
						alt={"preview"}
						width={320}
						src={targetImage}/>
					<Button 
						className={styles.clearButton}
						size={'small'}
						onClick={clearUpload}
						disabled={(countdown > 0 || targetImage == '')}
					>清除</Button>
				</div>
			</div>
			<div className={styles.vSeparate}></div>
			<div className={styles.question}>
				<Form
					name="formVisualQA"
					onFinish={onFinish}
					onFinishFailed={onFinishFailed}
					autoComplete="off"
				>
					<Form.Item label="问题" name="question">
						<div>
							<TextArea
								className={styles.questionInput}
								placeholder="请输入问题"/>
							<div className={styles.button}>
								<Button size={'small'} type="primary" htmlType="submit" disabled={countdown > 0}>
									{countdown > 0 ? `${countdown}s` : "查询"}
								</Button>
							</div>
						</div>
					</Form.Item>

				</Form>
				<Divider orientation="left"
								 className={`${styles.separate} ${answer != '' ? "" : styles.hide}`}>结果如下</Divider>
				<div className={`${styles.result} ${answer != "" ? "" : styles.hide}`}>
					<Typography>
						{answer.split('\n').map((line, index) => (
							<div key={index}>{line}</div>
						))}
					</Typography>
				</div>
			</div>
		</div>
	);
}

export default VisualQuestionAnswerByFile;
