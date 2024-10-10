"use client";

import {useEffect, useState} from "react";
import {ActionDemoChatCompletion, RequestChat} from "@/app/openapi/demo/chat";

const DemoCompletion = () => {
  const [text, setText] = useState<string>('');


  useEffect(() => {
    // console.log(question,llm,temperature)
    ActionDemoChatCompletion({
      name: "PowerX",
      message: "Hello"
    } as RequestChat).then((res) => {
      setText(res.message)
    });

  }, []);

  return (
    <div>
      <span>{text}</span>
    </div>
  )
}
export default DemoCompletion;
