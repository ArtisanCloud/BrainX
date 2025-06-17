import styles from './index.module.scss';
import React, {useContext, useEffect} from "react";
import {Button, Select} from 'antd';
import {MenuOutlined, MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons';
import {
  AppContextType,
  SelectedAppContext,

} from "@/app/(workspace)/space/workspace/robot-chat/provider/robot-chat-provider";
import {ProfileContext, ProfileContextType} from "@/app/(workspace)/space/(mine)/profile/provider/profile-provider";

import AppConfigModels from "../../../settings/model-provider/app-config-models";
import useSettingsStore from "@/app/store/setting";

const ChatNav = () => {
  const {selectedApp} = useContext(SelectedAppContext) as AppContextType;
  const {showProfile, setShowProfile} = useContext(ProfileContext) as ProfileContextType;
  const {fetchWorkspaceModels, fetchAllDefaultModels} = useSettingsStore();

  const toggleProfile = () => {
    // console.log("toggleProfile", showProfile)
    setShowProfile(!showProfile)
  }

  const openSetting = () => {
    console.log("openSetting")
  }


  useEffect(() => {
    // console.log("load models by types")
    fetchWorkspaceModels();
  }, []);

  useEffect(() => {
    fetchAllDefaultModels();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.info}>
        {/*<div className={styles.avatar}>*/}
        {/*  <Image width={42} height={42} alt={'avatar'} className={styles.avatarImage}*/}
        {/*         src={GetPublicUrl(selectedApp?.avatar_url!)}/>*/}
        {/*</div>*/}
        <div className={styles.content}>
          <div className={styles.titleBox}>
            <div className={styles.title}>{selectedApp?.name}</div>
            <AppConfigModels/>
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
