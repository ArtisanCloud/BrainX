import styles from './index.module.scss';
import React, {useContext, useState} from "react";
import {Form, Upload, FormProps, UploadProps, Image, Divider, Button} from 'antd';
import {InboxOutlined} from '@ant-design/icons';
import {ActionVisualSearch, RequestVisualSearch, ResponseVisualSearch} from "@/app/api/question-answer/visual-search";
import {ImageDocument} from "@/app/api/question-answer";
import useCountdown from "@/app/lib/countdown";
import {SelectLLMContext, SelectLLMContextType} from "@/app/components/space/provider/llm";

const {Dragger} = Upload;


const VisualSearch = () => {
	const [targetImage, setTargetImage] = useState<string>('');

	const [answers, setAnswers] = useState<ImageDocument[]>([]);
	const {selectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;
	const {countdown, startCountdown, stopCountdown} = useCountdown(0); // 倒计时时间，单位为秒

	const secondsCountDown = 60

	const props: UploadProps = {
		multiple: false,
		beforeUpload(file: any) {
			return new Promise((resolve) => {
				const reader = new FileReader();
				reader.readAsDataURL(file);
				reader.onload = () => {
					// console.log(reader.result);
					setTargetImage(reader.result as string);
				};
			});
		},
	};


	const onFinish: FormProps<RequestVisualSearch>["onFinish"] = async (values: RequestVisualSearch) => {

		values.llm = selectedLlm!
		values.question_image = targetImage

		try {
			// 如果提交验证成功，开始倒计时
			startCountdown(secondsCountDown)
			setAnswers([])
			const res = await ActionVisualSearch(values);
			if (res.image_documents.length > 0) {
				// res.answer = "根据描述的问题中，绝缘胶带粘贴困难。所以可以推断出当前存在问题。为了解决这个问题，需要更多的信息来确定根本原因和永久解决方案。\n\n提供的约束条件为：无、两处挡墙过窄以及V3.0改为灌胶等细节。\n\n建议: 在考虑根因时，请确认绝缘胶带粘贴是否涉及到特定的材料或环境因素（例如湿度）引起的困难。如果是由这些原因导致的，可以考虑改进工作环境来解决这个问题，比如保持适当的温度和湿度。如果根本原因是由于材料质量差或是操作不正确导致的问题，建议重新培训相关工作人员并提供正确的工具和技术指导以确保绝缘胶带粘贴顺利进行。\n\n总之，在面对绝缘胶带粘贴困难时，需要进一步调查问题的根本原因，并根据具体情况给出适当的解决方案来解决这个问题。"
				setAnswers(res.image_documents);
			}
		} catch (error) {
			console.error("请求失败:", error);
		} finally {
			stopCountdown(); // 无论请求成功或失败，都停止倒计时
		}
	};

	const onFinishFailed: FormProps<RequestVisualSearch>["onFinishFailed"] = (errorInfo: any) => {
		console.log('Failed:', errorInfo);
	};

	return (
		<div className={styles.container}>
			<Form
				name="formVisualSearch"
				// initialValues={{remember: true}}
				onFinish={onFinish}
				onFinishFailed={onFinishFailed}
				autoComplete="off"
				// className={styles.form}
			>
				<div className={styles.searchImage}>
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
					<div className={`${styles.preview} ${targetImage == '' ? styles.hide: '' }`}>
						<Image
							alt="上传的图片"
							width={320}
							src={targetImage}
						/>
					</div>
					<div className={styles.button}>
						<Button size={'small'}
										onClick={() => {
											setTargetImage('')
											setAnswers([])
										}}
										disabled={(countdown > 0 || targetImage == '')}
						>清除</Button>
						<Button
							size={'small'}
							type="primary"
							htmlType="submit"
							disabled={(countdown > 0 || targetImage == '')}>
							{countdown > 0 ? `${countdown}s` : "查询"}
						</Button>
					</div>
					<Divider orientation="left"
									 className={`${styles.separate} ${answers.length > 0 ? "" : styles.hide}`}>匹配结果如下</Divider>
					<div className={`${styles.result} ${answers.length > 0 ? "" : styles.hide}`}>
						{
							answers.map((answer, index) => {
								return (
									<div key={index} className={styles.imageDocument}>
										<Image
											alt={'匹配结果'}
											className={styles.image}
											src={`data:image/jpeg;base64,${answer.image}`}
										/>
										<span className={styles.content}>
										{answer.relative_document.text}
									</span>
									</div>
								);
							})
						}

					</div>
				</div>
			</Form>
		</div>
	);
}

export default VisualSearch;
