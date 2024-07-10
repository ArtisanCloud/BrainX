"use client";
import ArtisanCloudLogo from "@/app/ui/home/logo/index"
import React, {useEffect, useState} from "react";
import {
	Dropdown, DropdownItem, DropdownMenu, DropdownTrigger,
	Link,
} from "@nextui-org/react";
import Cookies from "js-cookie";
import {account_key, token_key} from "@/app/lib/auth";
import { Avatar } from 'antd';


export default function HomeNavbar() {

	const [loggedIn, setLoggedIn] = useState(false);
	const [account, setAccount] = useState('');

	useEffect(() => {
		// 在组件加载时检查用户是否已登录
		const checkLoginStatus = () => {
			const loggedIn = !!Cookies.get(token_key); // 根据自己的逻辑判断用户是否已登录
			setLoggedIn(loggedIn);
			setAccount(Cookies.get(account_key) || ''); // 获取用户账号
		};
		checkLoginStatus();
	}, []);

	const handleLogout = () => {
		// 处理用户退出登录
		Cookies.set(token_key, '', {expires: -1});
		setLoggedIn(false)
	};

	return (
		<div className={'h-24  bg-gradient-to-b-header  bg-bottom-100 bg-100x200 transition-all duration-500 w-full flex items-center px-7'}>
			<div className={'opacity-80'}>
				<ArtisanCloudLogo/>
			</div>
			<div className={'h-full flex gap-3 ml-auto mr-5'}>
				{loggedIn ? (
					<div className={"mt-6"}>
						<Dropdown placement="bottom-end">
							<DropdownTrigger>
								<Avatar style={{
									backgroundColor: '#af99d0',
									verticalAlign: 'middle',
									border: '#A283D2 solid 2px',
								}}
												size="large" gap={4}>
									{account}
								</Avatar>
							</DropdownTrigger>
							<DropdownMenu aria-label="Profile Actions" variant="flat">
								<DropdownItem key="profile" className="h-14 gap-2" textValue="account">
									<p className="font-semibold">{account}</p>
								</DropdownItem>
								<DropdownItem key="space" textValue="工作台">工作台</DropdownItem>
								<DropdownItem key="logout" onClick={handleLogout} color="danger" textValue="退出">
									退出
								</DropdownItem>
							</DropdownMenu>
						</Dropdown>
					</div>
				) : (
					<>
						<Link href={'/user/register'} className={'text-primary text-md font-bold opacity-65'}>注册</Link>
						<Link href={'/auth/login'} className={'text-primary text-md font-bold opacity-65 hover:text-foreground'}>登录</Link>
					</>
				)}
			</div>
		</div>
	);
}
