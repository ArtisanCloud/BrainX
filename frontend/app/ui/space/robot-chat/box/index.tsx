import styles from './index.module.scss';
import React, {useContext, useEffect, useRef, useState} from "react";
import {Button} from 'antd';
import {
	ControlOutlined,
	ExpandAltOutlined,
	PictureOutlined,
	MacCommandOutlined,
	EnterOutlined,
	AppstoreOutlined
} from '@ant-design/icons';
import useSSE from "@/app/lib/sse/EventSourceHelper";
import {Conversation, ConversationItem} from "@/app/api/robot-chat/conversation";
import {AppContextType, SelectedAppContext} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import {GetPublicUrl} from "@/app/lib/url";
import {GetChatBotSSEActionUrl} from "@/app/api/robot-chat";
import Image from "next/image";
import {SelectLLMContext, SelectLLMContextType} from "@/app/ui/space/provider/llm";
import ReactMarkdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';
import remarkGfm from 'remark-gfm';
import {FormatSSEMessageReply} from "@/app/lib/sse/format";


const ChatBox = () => {
	const {selectedApp} = useContext(SelectedAppContext) as AppContextType;
	const {selectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;

	const refInput = useRef<HTMLTextAreaElement>(null);
	const refMessageContainer = useRef<HTMLDivElement>(null);
	const [loading, setLoading] = useState<boolean>(false);
	const [showHint, setShowHint] = useState<boolean>(false);
	const [conversation, setConversation] = useState<Conversation>({
		currentPrompt: '',
		items: [
			{question: '', answer: '您好，请问有什么可以帮助到您？'},
			// { question: '有啥可以分享的？', answer: '没啥弄\n没啥弄\n没啥弄\n' },
			// { question: '吃了没？', answer: '我不饿' },
		],
	});

	const streamUrl = GetChatBotSSEActionUrl('chat');
	const sse = useSSE();

	const scrollToBottom = () => {
		refMessageContainer!.current!.scrollTo({
			top: refMessageContainer.current!.scrollHeight,
			behavior: 'smooth'
		});
	}

	useEffect(() => {
		scrollToBottom();
	}, [conversation]);

	const handleSelectModel = () => {
		console.log('select model');
	}

	const handleUploadImage = () => {
		console.log('upload image');
	}

	const handleClickSend = () => {
		if (!loading) {
			actionSend();
		}
	}
	const handleKeyDown = (event: any) => {
		if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
			// 执行发送消息的操作
			event.preventDefault();
			if (!loading) {
				actionSend();
			}
		}
	};

	const handleChatClosed = () => {
		// console.log('chat closed');
		setLoading(false);
		setShowHint(false);

		// // 清空 textarea
		// refInput.current!.value = '';

	}

	const actionSend = () => {

		refInput.current!.blur(); // 手动失去焦点

		// 执行发送消息的操作
		setLoading(true);
		const message = refInput.current!.value;
		if (message.trim() === '') {
			setShowHint(true);
			setLoading(false);
			return;
		} else {
			conversation.currentPrompt = message
		}
		// console.log('Send button clicked:', message);
		const newItem = {
			question: conversation.currentPrompt,
			answer: '',
		} as ConversationItem;

		setConversation((prevConversation) => ({
			...prevConversation,
			items: [...prevConversation.items, newItem],
		}));

		// 清空 textarea
		refInput.current!.value = '';

		sse.connectEventSource({
			url: streamUrl,
			method: 'POST',
			body: {
				conversationUUID: "",
				llm: selectedLlm,
				messages: [
					{
						role: 'user',
						content: conversation.currentPrompt,
					},
				],
			},
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
					// const objMsg = JSON.parse(msg.data);

					// <--- Add this check
					setConversation((prevConversation) => {
						const lastItem = prevConversation.items[prevConversation.items.length - 1];
						return {
							...prevConversation,
							items: prevConversation.items.map((item, index) =>
								index === prevConversation.items.length - 1
									? {...item, answer: item.answer + objMsg}
									: item
							),
						};
					});

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


	return (
		<div className={styles.container}>
			<div className={styles.messageContainer} ref={refMessageContainer}>
				{conversation.items.map((item: ConversationItem, index) => (
					<React.Fragment key={index}>
						{/* 用户消息单元 */}
						{item.question && (
							<div className={styles.userMessageCell}>
								<div className={styles.userAvatar}>
									<Image width={42} height={42} src={'/logo-s.png'} alt="User Avatar"/>
								</div>
								<div className={styles.message}>
									{/*{item.question}*/}
									<ReactMarkdown>{item.question}</ReactMarkdown>
								</div>
							</div>
						)}
						{/* AI 消息单元 */}
						<div className={styles.aiMessageCell}>
							<div className={styles.aiAvatar}>
								<Image width={42} height={42} src={GetPublicUrl(selectedApp?.avatar_url!)} alt="AI Avatar"/>
							</div>
							<div className={styles.message}>
								{loading && item.answer === '' ? (
									<span>...</span>
								) : (
									// <div dangerouslySetInnerHTML={{ __html: item.answer.replace(/\n/g, '<br>') }} />
									<ReactMarkdown
										remarkPlugins={[remarkGfm, remarkBreaks]}
									>
										{item.answer}
									</ReactMarkdown>
								)}
							</div>
						</div>
					</React.Fragment>
				))}
			</div>
			<div className={styles.inputContainer}>
				<div className={styles.inputTool}>
					<div className={styles.left}>
						<Button
							className={styles.buttonTool}
							onClick={handleSelectModel}
							size="small"
							icon={<AppstoreOutlined/>}/>
						<Button
							className={styles.buttonTool}
							onClick={handleUploadImage}
							disabled
							size="small"
							icon={<PictureOutlined/>}/>
						<Button
							className={styles.buttonTool}
							// onClick={openSetting}
							size="small"
							icon={<ControlOutlined/>}/>
					</div>
					<div className={styles.right}>
						<Button
							className={styles.buttonTool}
							// onClick={openSetting}
							size="small"
							icon={<ExpandAltOutlined/>}/>
					</div>

				</div>
				<div className={styles.inputMessage}>
					<textarea
						ref={refInput}
						className={`${styles.input} ${showHint ? styles.error : ''}`}
						placeholder={showHint ? '发送时，消息不能为空' : '请输入内容...'}
						disabled={loading}
						onKeyDown={handleKeyDown}
					/>
				</div>
				<div className={styles.inputCommand}>
					<span className={styles.shortCut}>
					快捷发送：<MacCommandOutlined/>/ctl + <EnterOutlined/>
					</span>
					<Button
						className={styles.sendButton}
						size={"small"}
						onClick={handleClickSend}
						disabled={loading}
					>Send</Button>
				</div>
			</div>

		</div>
	)
}
export default ChatBox
