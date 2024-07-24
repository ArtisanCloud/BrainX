// pages/auth/login.tsx
"use client";

import {Form, Input, Button, message} from 'antd';
import styles from './index.module.scss';
import HomeNavbar from "@/app/components/home/navbar";
import React from "react";
import {ActionLogin} from "@/app/api/auth";
import Cookies from 'js-cookie';
import {useRouter} from "next/navigation";
import {account_key, token_key} from "@/app/utils/auth";
import {encodePassword} from "@/app/lib/security";

export default function LoginPage() {

	const router = useRouter();
	const [messageApi, contextHolder] = message.useMessage();

	async function handleSubmit(values: { account: string; password: string }) {

		const response = await ActionLogin({
			account: values.account,
			password: encodePassword(values.password),
		});


		if (response.token) {
			// 设置cookie
			Cookies.set(token_key, response.token.access_token, {expires: response.token.expires_in * 1000});
			Cookies.set(account_key, response.account);
			// console.log(response.token)

			// 跳转到个人中心
			messageApi.info('登录成功');
			router.push('/space');

		} else {
			messageApi.error('登录失败:' + response.error);
		}
	}

	return (
		<div className={styles.container}>
			<div className={styles.formHeader}>
				<HomeNavbar/>
			</div>
			<div className={styles.formContainer}>
				<h2 className={styles.title}>登录</h2>
				<Form
					name="login"
					onFinish={handleSubmit}
					className={styles.form}
				>
					{contextHolder}
					<Form.Item
						name="account"
						rules={[{required: true, message: '请输入你的账号!'}]}
					>
						<Input placeholder="账号"
									 autoComplete="username"
									 className={styles.input}/>
					</Form.Item>
					<Form.Item
						name="password"
						rules={[{required: true, message: '请输入你的密码!'}]}
					>
						<Input.Password placeholder="密码"
														autoComplete="current-password"
														className={styles.input}/>
					</Form.Item>
					<Form.Item>
						<Button type="primary" htmlType="submit" className={styles.loginButton}>
							登录
						</Button>
					</Form.Item>
					<Form.Item>
						<Button href="/user/register" className={styles.registerButton}>
							注册
						</Button>
					</Form.Item>
				</Form>
			</div>
		</div>
	);
}
