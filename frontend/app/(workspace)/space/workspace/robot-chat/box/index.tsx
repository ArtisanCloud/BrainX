import styles from "./index.module.scss";
import React, { useContext, useEffect, useRef, useState } from "react";
import { Button, Image } from "antd";
import {
  ControlOutlined,
  ExpandAltOutlined,
  PictureOutlined,
  MacCommandOutlined,
  EnterOutlined,
  AppstoreOutlined,
  CloseOutlined,
} from "@ant-design/icons";
import useSSE from "@/app/lib/sse/EventSourceHelper";
import { ConversationItem } from "@/app/api/robot-chat/conversation";
import {
  AppContextType,
  SelectedAppContext,
  welcomeConversation,
} from "@/app/(workspace)/space/workspace/robot-chat/provider/robot-chat-provider";
import { GetPublicUrl } from "@/app/lib/url";
import { GetChatBotSSEActionUrl, RequestSendChat } from "@/app/api/robot-chat";
import {
  SelectLLMContext,
  SelectLLMContextType,
} from "@/app/(workspace)/space/(mine)/provider/llm";

import { FormatSSEMessageReply, SSEMessage } from "@/app/lib/sse/format";
import { v4 as uuidv4 } from "uuid";
import MarkdownPreview from "@/app/(workspace)/space/workspace/robot-chat/markdown/markdown";
import { useNotification } from "@/app/components/notification";

const ChatBox = () => {
  const { selectedApp, currentConversation, setCurrentConversation } =
    useContext(SelectedAppContext) as AppContextType;
  const { selectedLlm } = useContext(SelectLLMContext) as SelectLLMContextType;

  const refInput = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedImage, setSelectedImage] = useState<string>("");
  const { msgSuccess, msgWarn, msgError } = useNotification();

  const refMessageContainer = useRef<HTMLDivElement>(null);
  const [aiProcessing, setAIProcessing] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const [showHint, setShowHint] = useState<boolean>(false);
  // const [conversation, setConversation] = useState<Conversation>(welcomeConversation);

  // const streamUrl = GetChatBotSSEActionUrl('chat');
  let streamUrl = GetChatBotSSEActionUrl("agent/chat");
  const sse = useSSE();
  let controller: any = null;

  const scrollToBottom = () => {
    refMessageContainer!.current!.scrollTo({
      top: refMessageContainer.current!.scrollHeight,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    setCurrentConversation(welcomeConversation);
  }, [selectedApp, setCurrentConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation]);

  const handleSelectModel = () => {
    console.log("select model");
  };

  // 添加处理文件选择的函数
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // 检查文件类型
      if (!file.type.startsWith("image/")) {
        msgError("请选择图片文件");
        return;
      }

      // 检查文件大小（例如限制为 5MB）
      if (file.size > 5 * 1024 * 1024) {
        msgError("图片大小不能超过 5MB");
        return;
      }

      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        setSelectedImage(reader.result as string);
      };
    }
  };

  const handleImagesClear = () => {
    setSelectedImage("");
    // 重置 Upload 组件的状态
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUploadImage = () => {
    fileInputRef.current?.click();
  };

  const handleClickSend = () => {
    if (!loading) {
      actionSend();
    }
  };
  const handleKeyDown = (event: any) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
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
    handleImagesClear()

    // // 清空 textarea
    // refInput.current!.value = '';
    controller.abort();
  };

  const actionSend = () => {
    if (loading) return;

    refInput.current!.blur(); // 手动失去焦点

    // 如果是随意聊天模式
    if (!selectedApp?.uuid) {
      streamUrl = GetChatBotSSEActionUrl("chat");
    }

    // 执行发送消息的操作
    setLoading(true);
    const message = refInput.current!.value;
    if (message.trim() === "") {
      setShowHint(true);
      setLoading(false);
      return;
    } else {
      currentConversation.currentPrompt = message;
    }
    // console.log('Send button clicked:', message);
    const newItem = {
      question: currentConversation.currentPrompt,
      answer: "",
    } as ConversationItem;

    // 初始化一个uuid，给conversation
    let sessionID = "";
    if (!currentConversation.uuid || currentConversation.uuid == "") {
      sessionID = uuidv4();
    } else {
      sessionID = currentConversation.uuid!;
    }
    // 小心，别冲突了
    setCurrentConversation((prevConversation) => ({
      ...prevConversation,
      uuid: sessionID,
      items: [...prevConversation.items, newItem],
    }));

    // 清空 textarea
    refInput.current!.value = "";

    const requestBody: RequestSendChat = {
      conversationUUID: sessionID,
      appUUID: selectedApp?.uuid ?? "",
      llm: selectedLlm ?? "",
      images: selectedImage ? [selectedImage] : [], // 如果有图片则添加到请求中
      messages: [
        {
          type: "user",
          role: 'user',
          content: currentConversation.currentPrompt,
        },
      ],
    };
    // console.log('actionSend requestBody:', requestBody);
    controller = sse.connectEventSource({
      url: streamUrl,
      method: "POST",
      body: requestBody,
      onopen(response: Response) {
        // 滑向下方
        // scrollToBottom()
        // console.log('onopen', response);

        // Handle successful connection
        if (response.status === 200) {
          // console.log('sse response', response.statusText);
        }
      },
      onmessage(msg: any) {
        // Handle incoming messages
        // console.log('msg', msg);
        try {
          let objMsg = "";
          let errorMessage = "";
          const parsedMsg: SSEMessage = JSON.parse(msg.data);
          if (parsedMsg.status == "processing") {
            setAIProcessing(true);
            return;
          } else {
            setAIProcessing(false);

            if (parsedMsg.status == "data") {
              objMsg = FormatSSEMessageReply(parsedMsg.content);
            } else if (parsedMsg.status == "error") {
              errorMessage = parsedMsg.message;
            } else if (parsedMsg.status == "finished") {
              handleChatClosed();
              return;
            }
          }

          // const objMsg = JSON.parse(msg.data);

          // <--- Add this check
          setCurrentConversation((prevConversation) => {
            const lastItem =
              prevConversation.items[prevConversation.items.length - 1];
            return {
              ...prevConversation,
              items: prevConversation.items.map((item, index) =>
                index === prevConversation.items.length - 1
                  ? {
                      ...item,
                      answer: item.answer + objMsg,
                      errorMessage: errorMessage,
                    }
                  : item
              ),
            };
          });
        } catch (error) {
          console.error("Error parsing JSON data:", error);
          handleChatClosed();
        } finally {
        }
      },
      onclose() {
        // Handle connection closed
        // console.log('sse close');
        handleChatClosed();
      },
      onerror(err: any) {
        // Handle errors
        console.error("err", err);
        if (err) {
          handleChatClosed();
        }
      },
    });
  };

  return (
    <div className={styles.container}>
      <div className={styles.messageContainer} ref={refMessageContainer}>
        {currentConversation.items.map((item: ConversationItem, index) => (
          <React.Fragment key={index}>
            {/* 用户消息单元 */}
            {item.question && (
              <div className={styles.userMessageCell}>
                <div className={styles.userAvatar}>
                  <Image
                    width={42}
                    height={42}
                    src={"/images/logo-s.png"}
                    alt="User Avatar"
                  />
                </div>
                <div className={styles.message}>
                  {/*{item.question}*/}
                  <MarkdownPreview markdownText={item.question} />
                </div>
              </div>
            )}
            {/* AI 消息单元 */}
            <div className={styles.aiMessageCell}>
              <div className={styles.aiAvatar}>
                <Image
                  width={42}
                  height={42}
                  src={GetPublicUrl(selectedApp?.avatar_url!)}
                  alt="AI Avatar"
                  style={{ maxWidth: "42px", objectFit: "cover" }}
                />
              </div>
              <div className={styles.message}>
                {loading && aiProcessing && item.answer === "" ? (
                  <span>...</span>
                ) : item.errorMessage ? (
                  // 显示错误信息
                  <div className={styles.error}>{item.errorMessage}</div>
                ) : (
                  // 显示答案或 markdown 内容
                  <section className={styles.markdownContent}>
                    <MarkdownPreview markdownText={item.answer} />
                  </section>
                )}
              </div>
            </div>
          </React.Fragment>
        ))}
      </div>
      <div className={styles.inputContainer}>
        {/* 添加隐藏的文件输入 */}
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: "none" }}
          accept="image/*"
          onChange={handleFileSelect}
        />
        {/* 添加图片预览区域 */}
        {selectedImage && (
          <div className={styles.imagePreview}>
            <div className={styles.previewContent}>
              <Image
                src={selectedImage}
                alt="Preview"
                width={60}
                height={60}
                style={{ objectFit: "cover" }}
              />
              <Button
                type="text"
                size="small"
                onClick={handleImagesClear}
                icon={<CloseOutlined />}
              />
            </div>
          </div>
        )}
        <div className={styles.inputTool}>
          <div className={styles.left}>
            <Button
              className={styles.buttonTool}
              onClick={handleSelectModel}
              size="small"
              icon={<AppstoreOutlined />}
            />
            <Button
              className={styles.buttonTool}
              onClick={handleUploadImage}
              size="small"
              icon={<PictureOutlined />}
            />
            <Button
              className={styles.buttonTool}
              // onClick={openSetting}
              size="small"
              icon={<ControlOutlined />}
            />
          </div>
          <div className={styles.right}>
            <Button
              className={styles.buttonTool}
              // onClick={openSetting}
              size="small"
              icon={<ExpandAltOutlined />}
            />
          </div>
        </div>
        <div className={styles.inputMessage}>
          <textarea
            ref={refInput}
            className={`${styles.input} ${showHint ? styles.error : ""}`}
            placeholder={showHint ? "发送时，消息不能为空" : "请输入内容..."}
            disabled={loading}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className={styles.inputCommand}>
          <span className={styles.shortCut}>
            快捷发送：
            <MacCommandOutlined />
            /ctl + <EnterOutlined />
          </span>
          <Button
            className={styles.sendButton}
            size={"small"}
            onClick={handleClickSend}
            disabled={loading}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};
export default ChatBox;
