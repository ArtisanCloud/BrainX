import styles from './index.module.scss';
import React, {useContext} from "react";
import {Button, Select} from 'antd';
import {MenuOutlined, MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons';
import {
  AppContextType,
  SelectedAppContext,

} from "@/app/(workspace)/space/workspace/robot-chat/provider/robot-chat-provider";
import {GetPublicUrl} from "@/app/lib/url";
import {ProfileContext, ProfileContextType} from "@/app/(workspace)/space/(mine)/profile/provider/profile-provider";
import Image from "next/image";
import {SelectLLMContext, SelectLLMContextType} from "@/app/(workspace)/space/(mine)/provider/llm";
import {
  baidu_ernie_lite_8k,
  baidu_ernie_speed_128k,
  baidu_qianfan_bloomz_7b_compressed,
  baidu_qianfan_ernie_3_d_5_8k,
  baidu_qianfan_ernie_4_d_0_8k, doubao_lite_32k, kimi_moonshot_v1_8k, label_baidu_ernie_lite_8k,
  label_baidu_ernie_speed_128k,
  label_baidu_qianfan_bloomz_7b_compressed,
  label_baidu_qianfan_ernie_3_d_5_8k,
  label_baidu_qianfan_ernie_4_d_0_8k,
  label_doubao_lite_32k,
  label_kimi_moonshot_v1_8k,
  label_ollama_13b_alpaca_16k, label_ollama_deepseek_r1_1_5b, label_ollama_deepseek_r1_70b,
  label_ollama_gemma_2b, label_ollama_llama3_2, label_ollama_llama3_3,
  label_ollama_qwen_2_5,
  label_ollama_qwen_2_5_72b,
  label_openai_gpt_3_d_5_turbo,
  label_openai_gpt_4_o,
  label_tencent_hunyuan_lite,
  label_tencent_hunyuan_standard,
  label_tencent_hunyuan_turbo,
  ollama_13b_alpaca_16k, ollama_deepseek_r1_1_5b, ollama_deepseek_r1_70b,
  ollama_gemma_2b, ollama_llama3_2, ollama_llama3_3,
  ollama_qwen_2_5,
  ollama_qwen_2_5_72b,
  openai_gpt_3_d_5_turbo,
  openai_gpt_4_o,
  tencent_hunyuan_lite,
  tencent_hunyuan_standard,
  tencent_hunyuan_turbo
} from "@/app/config/llm";

const ChatNav = () => {
  const {setSelectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;
  const {selectedApp} = useContext(SelectedAppContext) as AppContextType;
  const {showProfile, setShowProfile} = useContext(ProfileContext) as ProfileContextType;


  const toggleProfile = () => {
    // console.log("toggleProfile", showProfile)
    setShowProfile(!showProfile)
  }

  const openSetting = () => {
    console.log("openSetting")
  }

  const handleChangeLLM = (e: any) => {
    // console.log("handleChangeLLM", e.value)
    setSelectedLlm(e.value)

  }

  return (
    <div className={styles.container}>
      <div className={styles.info}>
        <div className={styles.avatar}>
          <Image width={42} height={42} alt={'avatar'} className={styles.avatarImage}
                 src={GetPublicUrl(selectedApp?.avatar_url!)}/>
        </div>
        <div className={styles.content}>
          <div className={styles.titleBox}>
            <div className={styles.title}>{selectedApp?.name}</div>
            <div className={styles.title}>
              <Select
                className={styles.selectLLM}
                labelInValue
                style={{border: "none"}}
                // defaultValue={{value: openai_gpt_3_d_5_turbo, label: label_openai_gpt_3_d_5_turbo}}
                defaultValue={{value: baidu_ernie_lite_8k, label: label_baidu_ernie_lite_8k}}
                onChange={handleChangeLLM}
                options={[
                  {
                    label: label_openai_gpt_3_d_5_turbo,
                    value: openai_gpt_3_d_5_turbo,
                  },
                  {
                    label: label_ollama_deepseek_r1_1_5b,
                    value: ollama_deepseek_r1_1_5b,
                  },
                  {
                    label: label_ollama_deepseek_r1_70b,
                    value: ollama_deepseek_r1_70b,
                  },
                  {
                    label: label_openai_gpt_4_o,
                    value: openai_gpt_4_o,
                  },
                  {
                  	label: label_baidu_qianfan_ernie_4_d_0_8k,
                  	value: baidu_qianfan_ernie_4_d_0_8k
                  },
                  {
                  	label: label_baidu_qianfan_ernie_3_d_5_8k,
                  	value: baidu_qianfan_ernie_3_d_5_8k
                  },
                  // {
                  // 	label: label_baidu_qianfan_bloomz_7b_compressed,
                  // 	value: baidu_qianfan_bloomz_7b_compressed,
                  // },
                  // {
                  // 	label: label_baidu_ernie_speed_128k,
                  // 	value: baidu_ernie_speed_128k,
                  // },
                  {
                    label: label_baidu_ernie_lite_8k,
                    value: baidu_ernie_lite_8k,
                  },
                  {
                    label: label_tencent_hunyuan_turbo,
                    value: tencent_hunyuan_turbo,
                  },
                  {
                    label: label_tencent_hunyuan_standard,
                    value: tencent_hunyuan_standard,
                  },
                  {
                    label: label_tencent_hunyuan_lite,
                    value: tencent_hunyuan_lite,
                  },
                  {
                    label: label_ollama_llama3_2,
                    value: ollama_llama3_2,
                  },
                  {
                    label: label_ollama_llama3_3,
                    value: ollama_llama3_3,
                  },
                  {
                    label: label_ollama_qwen_2_5,
                    value: ollama_qwen_2_5,
                  },
                  {
                    label: label_ollama_qwen_2_5_72b,
                    value: ollama_qwen_2_5_72b,
                  },
                  // {
                  //   label: label_ollama_gemma_2b,
                  //   value: ollama_gemma_2b,
                  // },
                  {
                    label:label_kimi_moonshot_v1_8k,
                    value:kimi_moonshot_v1_8k
                  },
                  {
                    label:label_doubao_lite_32k,
                    value:doubao_lite_32k
                  }
                ]}
              />
            </div>
          </div>
          <div className={styles.description}>{selectedApp?.description}</div>
        </div>
      </div>
      <div className={styles.action}>
        <Button
          className={styles.showSetting}
          onClick={toggleProfile}
          size="small"
          icon={showProfile ? <MenuUnfoldOutlined/> : <MenuFoldOutlined/>}
        />

        <Button
          className={styles.openSetting}
          onClick={openSetting}
          size="small"
          icon={<MenuOutlined/>}/>
      </div>

    </div>
  )
}
export default ChatNav
