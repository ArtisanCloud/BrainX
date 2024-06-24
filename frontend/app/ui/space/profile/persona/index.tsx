import React, {forwardRef, Ref, useContext, useImperativeHandle} from 'react';
import styles from './index.module.scss';
import {useState} from "react";
import {ActionPatchApp, App, ResponseCreateApp} from "@/app/api/robot-chat/app";
import {Modal, message} from "antd"
import SetPersona from "@/app/ui/space/profile/persona/set-persona/index";
import {CreateAppContext, CreateAppContextType} from "@/app/ui/space/app/provider/create-app-provider";
import {hintAppPersona} from "@/app/config/constant/placeholder";


interface Props {
	app: App;
}

export type RefPersona = {
	onHandleEdit: () => void;
};

const Persona = forwardRef<RefPersona, Props & { ref?: Ref<RefPersona> }>((props, ref) => {
	const {
		persona,
		setPersona,
	} = useContext(CreateAppContext) as CreateAppContextType;
	const [messageApi, contextHolder] = message.useMessage();
	const [loading, setLoading] = useState(false);
	const [isModalOpen, setIsModalOpen] = useState(false);


	useImperativeHandle(ref, () => ({
		onHandleEdit: () => {
			handleEdit();
		}
	}));

	const handleEdit = () => {
		// console.log("handleEdit", props.app)
		setIsModalOpen(true);
	}

	const handleOk = async () => {
		// console.log(name, description, avatarUrl)

		if (loading) {
			return
		}
		// console.log(persona)
		const res: ResponseCreateApp = await ActionPatchApp({
			uuid: props.app.uuid,
			persona_prompt: persona!,
		})

		setLoading(false);

		if (res.error && res.error !== "") {
			messageApi.error('设置智能领域人格失败:' + res.error);
		} else {
			messageApi.info('设置智能领域人格成功');
		}

		setIsModalOpen(false);

	};

	return (
		<div className={styles.container}>
			<div className={styles.content} onClick={handleEdit}>
				{props.app.persona_prompt ? props.app.persona_prompt : hintAppPersona}
			</div>
			{contextHolder}
			<Modal
				style={{top: 120}}
				title="创建机器人"
				open={isModalOpen}
				onOk={handleOk}
				onCancel={() => setIsModalOpen(false)}
			>
				<SetPersona app={props.app} />
			</Modal>
		</div>
	);
});


Persona.displayName = 'Persona'; // Add this line

export default Persona;
