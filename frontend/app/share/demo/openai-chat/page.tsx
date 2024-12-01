"use client";

import styles from "./index.module.scss";
import classnames from "classnames";
import { Fragment, useEffect, useRef, useState } from "react";

import { Form, Divider, FormProps, Typography } from "antd";
import useSSE from "@/app/lib/sse/EventSourceHelper";
import { baidu_ernie_lite_8k } from "@/app/config/llm";
import { FormatSSEMessageReply, SSEMessage } from "@/app/lib/sse/format";
import { GetOpenAPIChatBotSSEActionUrl, SSEOpenAIMessage } from "@/app/openapi/robot_chat";
import { RequestSendOpenAIChat } from "@/app/openapi/robot_chat/openai";

const DemoOpenAIChatPage = () => {
  const [answer, setAnswer] = useState<string>("");
  const [selectedLlm, setSelectedLlm] = useState<string>(baidu_ernie_lite_8k);

  const [loading, setLoading] = useState<boolean>(false);

  const streamUrl = GetOpenAPIChatBotSSEActionUrl("agent/openai/chat");
  const sse = useSSE();

  const formRef = useRef<any>(null); // 使用useRef保存Form的引用

  const onFinish: FormProps<RequestChat>["onFinish"] = async (
    values: RequestChat
  ) => {
    // console.log(loading)
    if (!loading) {
      values.question = formRef.current.question;
      values.llm = formRef.current.llm;
      values.temperature = formRef.current.temperature;
      // values.llm = selectedLlm!
      console.log("onFinish value:", values);
      actionSend(values);
    }

    // console.log('Success:', values.question);
  };

  const onFinishFailed: FormProps<RequestChat>["onFinishFailed"] = (
    errorInfo: any
  ) => {
    console.log("Failed:", errorInfo);
  };

  const handleChatClosed = () => {
    // console.log('chat closed');
    setLoading(false);

    // // 清空 textarea
    // refInput.current!.value = '';
  };

  const actionSend = (values: RequestChat) => {
    // 执行发送消息的操作
    setLoading(true);
    const message = values.question;
    if (message.trim() === "") {
      setLoading(false);
      return;
    }

    if (!selectedLlm) {
      console.error("No selected LLM");
      return;
    }

    sse.connectEventSource({
      url: streamUrl,
      method: "POST",
      body: {
        conversation_uuid: "",
        app_uuid: "7c189a18-ef3f-41fd-bda1-1607772020bd",
        model: values.llm,
        images: [],
        messages: [
          {
            type: "user",
            role: "user",
            content: values.question,
          },
        ],
        temperature: values.temperature,
      } as RequestSendOpenAIChat,
      token:
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX2FjY2Vzc19rZXkiOiJrZXlfcG93ZXJfeCIsIm5hbWUiOiJwb3dlcngiLCJleHAiOjE3MzU0NDExNjB9.GEyJaXs9Ul4MCwjSKckCsKZAh_BMWapMzONAX1_ZDnc",
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
        try {
          let objMsg = "";
          let errorMessage = "";
		  console.log(msg)
          const parsedMsg: SSEOpenAIMessage = JSON.parse(msg.data);
		//   console.log("parsedMsg", parsedMsg);
          if (parsedMsg.status == "processing") {
            return;
          } else {
            if (parsedMsg.status == "error") {
              errorMessage = parsedMsg.choices[0].message.content;
            } else if (parsedMsg.status == "finished") {
              handleChatClosed();
              return;
            }else{
				objMsg = FormatSSEMessageReply(parsedMsg.choices[0].message.content);
				setAnswer((prevAnswer) => prevAnswer + objMsg);
			}
          }
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

  useEffect(() => {
    // console.log(question,llm,temperature)
    const params = new URLSearchParams(window.location.search);
    const question = params.get("question") || "";
    const llm = params.get("llm") || baidu_ernie_lite_8k;
    const temperature = parseFloat(params.get("temperature")!) || 0.5;

    formRef.current.question = question;
    formRef.current.llm = llm;
    formRef.current.temperature = temperature;
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
      ></Form>

      <div
        className={classnames(styles.result, {
          [styles.hide]: answer === "",
        })}
      >
        <Divider orientation="left" className={styles.separate}>
          请看如下结果:
        </Divider>
        <Typography style={{ fontSize: "12px" }}>
          {answer.split("\n").map((line, index) => (
            <Fragment key={index}>
              {line}
              {index !== answer.split("\n").length - 1 && <br />}
            </Fragment>
          ))}
        </Typography>
      </div>
    </div>
  );
};

export default DemoOpenAIChatPage;
