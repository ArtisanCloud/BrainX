"use client";

import styles from './index.module.scss'
import {Input} from 'antd';
import {forwardRef, Ref, useContext, useEffect} from "react";
import {CreateAppContext, CreateAppContextType} from "@/app/components/space/app/provider/create-app-provider";
import {hintAppPersona} from "@/app/config/constant/placeholder";
import {App} from "@/app/api/app";
import {RefPersona} from "@/app/components/space/profile/persona";


const {TextArea} = Input;

interface Props {
	app: App;
}

const SetPersona = forwardRef<HTMLDivElement, Props>((props: Props, ref) => {
	const {
		persona,
		setPersona,
	} = useContext(CreateAppContext) as CreateAppContextType;

	// 需要清空一下之前的person
	useEffect(() => {
		setPersona("")
	}, [setPersona]);

	const handleChangePersona = (e: any) => {
		// 先要本地的值能够能改动
		props.app.persona = e.target.value
		// 然后在context里保存修改的值
		setPersona(e.target.value)
	}

	return (
		<div ref={ref} className={styles.container}>
			<TextArea onChange={handleChangePersona} value={props.app?.persona}
								placeholder={hintAppPersona}
								rows={28}/>
		</div>
	);
});

SetPersona.displayName = "SetPersona"

export default SetPersona
