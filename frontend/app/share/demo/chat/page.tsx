"use client"

import styles from './index.module.scss';
import classnames from "classnames";
import {Fragment, useEffect, useRef, useState} from "react";

import {Form, Divider, Input, FormProps, Typography} from 'antd';
import {GetDemoChatSSEActionUrl, RequestChat} from "@/app/api/demo/chat";
import useSSE from "@/app/lib/sse/EventSourceHelper";
import {baidu_ernie_lite_8k, baidu_qianfan_ernie_3_d_5_8k} from "@/app/config/llm";
import {FormatSSEMessageReply} from "@/app/lib/sse/format";

const DemoChatPage = () => {
	const [answer, setAnswer] = useState<string>('');
	const [selectedLlm, setSelectedLlm] = useState<string>(baidu_ernie_lite_8k);

	const [loading, setLoading] = useState<boolean>(false);

	const streamUrl = GetDemoChatSSEActionUrl('chat');
	const sse = useSSE();

	const formRef = useRef<any>(null); // 使用useRef保存Form的引用

	const onFinish: FormProps<RequestChat>["onFinish"] = async (values: RequestChat) => {
		// console.log(loading)
		if (!loading) {

			values.question = formRef.current.question
			values.llm = formRef.current.llm
			values.temperature = formRef.current.temperature
			// values.llm = selectedLlm!
			console.log("onFinish value:", values)
			actionSend(values);
		}

		// console.log('Success:', values.question);

	};

	const onFinishFailed: FormProps<RequestChat>["onFinishFailed"] = (errorInfo: any) => {
		console.log('Failed:', errorInfo);
	};

	const handleChatClosed = () => {
		// console.log('chat closed');
		setLoading(false);

		// // 清空 textarea
		// refInput.current!.value = '';

	}

	const actionSend = (values: RequestChat) => {

		// 执行发送消息的操作
		setLoading(true);
		const message = values.question;
		if (message.trim() === '') {
			setLoading(false);
			return;
		}

		if (!selectedLlm) {
			console.error('No selected LLM')
			return;
		}

		sse.connectEventSource({
			url: streamUrl,
			method: 'POST',
			body: {
				question: values.question,
				llm: values.llm,
				temperature: values.temperature,
			} as RequestChat,
			onopen(response: any) {
				// 滑向下方
				// scrollToBottom()

				// Handle successful connection
				if (response.status === 200) {
					// console.log('sse response', response.statusText);
				}

			},
			onmessage(msg: any) {
				// Handle incoming messages
				// console.log('msg', msg);
				const objMsg = FormatSSEMessageReply(msg.data)
				try {
					try {
						setAnswer(prevAnswer => prevAnswer + objMsg);
					} catch (error) {
						console.error('Error parsing JSON data:', error);
					}
				} catch (error) {
					console.error('Error parsing JSON data:', error);
				}

			},
			onclose() {
				// Handle connection closed
				// console.log('sse close');
				handleChatClosed();
			},
			onerror(err: any) {
				// Handle errors
				console.error('err', err);
				if (err) {
					handleChatClosed()
				}
			},
		});
	}

	useEffect(() => {
		// console.log(question,llm,temperature)
		const params = new URLSearchParams(window.location.search);
		const question = params.get('question') || '';
		const llm = params.get('llm') || baidu_ernie_lite_8k;
		const temperature = parseFloat(params.get('temperature')!) || 0.5;

		formRef.current.question = question
		formRef.current.llm = llm
		formRef.current.temperature = temperature
		// console.log(formRef.current)
		formRef.current.submit();

	}, []);

	return (
		<div className={styles.container}>
			<Form
				ref={formRef}
				name="formConclustion"
				// initialValues={{remember: true}}
				onFinish={onFinish}
				onFinishFailed={onFinishFailed}
				autoComplete="off"
				// className={styles.form}
			>

			</Form>


			<div className={classnames(
				styles.result,
				{
					[styles.hide]: answer === ""
				}
			)}>
				<Divider orientation="left" className={styles.separate}>请看如下结果:</Divider>
				<Typography style={{fontSize:"12px"}}>
					{answer.split('\n').map((line, index) => (
						<Fragment key={index}>
							{line}
							{index !== answer.split('\n').length - 1 && <br />}
						</Fragment>
					))}
				</Typography>
			</div>


		</div>
	);
}

export default DemoChatPage;
