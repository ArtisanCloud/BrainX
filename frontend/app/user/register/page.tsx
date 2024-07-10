// pages/user/register.tsx
"use client";

import {Form, Input, Button, message} from 'antd';
import styles from './index.module.scss';
import {useRouter} from "next/navigation";
import HomeNavbar from '@/app/ui/home/navbar';
import React from "react";
import {ActionRegister} from "@/app/api/auth";

export default function RegisterPage() {

	const router = useRouter();
	const [messageApi, contextHolder] = message.useMessage();

	async function handleSubmit(values: { account: string; password: string }) {
		const response = await ActionRegister({
			account: values.account,
			password: values.password,
		});

		if (response.user) {
			messageApi.info('注册成功');
			router.push('/login');
		}else{
			messageApi.error('注册失败:' + response.error);
		}
	}

	return (
		<div className={styles.container}>
			<div className={styles.formHeader}>
				<HomeNavbar/>
			</div>
			<div className={styles.formContainer}>
				<h2 className={styles.title}>注册</h2>
				<Form name="register" onFinish={handleSubmit} className={styles.form}>
					<Form.Item
						name="account"
						rules={[{required: true, message: '请输入你的邮箱!'}]}
					>
						<Input placeholder="Email" className={styles.input}/>
					</Form.Item>
					<Form.Item
						name="password"
						rules={[{required: true, message: '请输入你的密码!'}]}
					>
						<Input.Password placeholder="Password" className={styles.input}/>
					</Form.Item>
					<Form.Item>
						<Button type="primary" htmlType="submit" className={styles.registerButton}>
							注册
						</Button>
					</Form.Item>
					<Form.Item>
						<Button href="/user/login" className={styles.loginButton}>
							返回登录
						</Button>
					</Form.Item>
				</Form>
			</div>
		</div>
	);
}
