import styles from './index.module.scss';
import {Collapse, Divider} from 'antd';
import {
	ProfileContext,
	ProfileContextType,
} from "@/app/components/space/profile/provider/profile-provider";
import {FormOutlined, PlusOutlined} from '@ant-design/icons';

import {useContext, useEffect, useRef, useState} from "react";
import {ItemType} from 'rc-collapse/es/interface';
import Persona, {RefPersona} from "@/app/components/space/profile/persona";
import {AppContextType, SelectedAppContext} from "@/app/components/space/robot-chat/provider/robot-chat-provider";
import CreateAppProvider from "@/app/components/space/app/provider/create-app-provider";

const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
`;


const ChatProfile = () => {

	const refPerson = useRef<RefPersona>(null);
	const context = useContext(SelectedAppContext) as AppContextType
	const selectedApp = context ? context.selectedApp : null;

	const handleEditPersona = () => (
		<FormOutlined
			style={{color: '#aaa', fontSize: '10px'}}
			onClick={(event: any) => {
				// If you don't want click extra trigger collapse, you can prevent this:
				// console.log(refPerson.current);
				if (refPerson.current) {
					refPerson.current.onHandleEdit(); // Call the onEdit method of the child component
					// If you don't want click extra trigger collapse, you can prevent this:
					event.stopPropagation();
				}

			}}
		/>
	);
	const genExtra = () => (
		<PlusOutlined
			style={{color: '#aaa', fontSize: '10px'}}
			onClick={(event: any) => {
				// If you don't want click extra trigger collapse, you can prevent this:
				event.stopPropagation();
			}}
		/>
	);

	type ProfileItem = {
		[key: string]: ItemType[] | undefined;
	}

	const profileItems: ProfileItem = {
		Context: [
			{
				key: 'persona',
				label: '人设和路由',
				children: (
					<CreateAppProvider>
						<Persona ref={refPerson} app={selectedApp!}/>
					</CreateAppProvider>
				),
				extra: handleEditPersona(),
			},
		] as ItemType[],

		Skill: [
			{
				key: 'plugin',
				label: '插件',
				children: <div>{text}</div>,
				extra: genExtra(),
			},
			{
				key: 'workflow',
				label: '工作流',
				children: <div>{text}</div>,
				extra: genExtra(),
			}
		] as ItemType[],

		Knowledge: [
			{
				key: 'knowledge',
				label: '知识库',
				children: <div>{text}</div>,
				extra: genExtra(),
			}
		] as ItemType[],
		Memory: [
			{
				key: 'database',
				label: '数据库',
				children: <div>{text}</div>,
				extra: genExtra(),
			},
			{
				key: 'long-term-memory',
				label: '长期记忆',
				children: <div>开启后，会总结对话的内容，在增强机器人对此次对话的理解。</div>,
				extra: genExtra(),
			},
			{
				key: 'variable',
				label: '变量',
				children: <div>{text}</div>,
				extra: genExtra(),
			}
		] as ItemType[],
		Character: [
			{
				key: 'voice',
				label: '声音',
				children: <div>{text}</div>,
				extra: genExtra(),
			},
			{
				key: 'hobby',
				label: '兴趣',
				children: <div>{text}</div>,
				extra: genExtra(),
			},
		] as ItemType[]
	};

	const {showProfile} = useContext(ProfileContext) as ProfileContextType;

	const [containerClassName, setContainerClassName] = useState('');

	useEffect(() => {
		// 根据 selectedApp 的值设置 containerClassName
		const newClassName = `${styles.container} ${showProfile ? styles.show : styles.hide}`;
		setContainerClassName(newClassName);
		// console.log(containerClassName)
	}, [showProfile]);

	const onChange = (key: string | string[]) => {
		// console.log(key);
	};

	const profileItemKeys = Object.keys(profileItems);

	return (
		<div className={selectedApp?.name == "纯聊天" ? styles.hide : containerClassName}>
			<div className={styles.list}>
				{profileItemKeys.map((key, index) => (
					<div key={key} className={styles.profileItem}>
						<Divider className={styles.divider} orientation="left">{key}</Divider>
						<Collapse
							style={{
								fontSize: '12px',
							}}
							key={key}
							defaultActiveKey={['Context']}
							onChange={onChange}
							// variant="borderless"
							expandIconPosition={'start'}
							items={profileItems[key] as ItemType[]}
						/>
					</div>
				))}
			</div>
		</div>
	)
}
export default ChatProfile
