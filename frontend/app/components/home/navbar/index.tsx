"use client";
import ArtisanCloudLogo from "@/app/components/home/logo/index"
import React, {useEffect, useState} from "react";
import {
	Dropdown, DropdownItem, DropdownMenu, DropdownTrigger,
	Link,
} from "@nextui-org/react";
import Cookies from "js-cookie";
import { token_key} from "@/app/utils/auth";
import { Avatar } from 'antd';
import useSessionStore from "@/app/store/session";


export default function HomeNavbar() {

	const {  sessionLogout, user, isLoggedIn } = useSessionStore();


	const handleLogout = () => {
		// 处理用户退出登录
		sessionLogout()
	};

	return (
		<div className={'h-24  bg-gradient-to-b-header  bg-bottom-100 bg-100x200 transition-all duration-500 w-full flex items-center px-7'}>
			<div className={'opacity-80'}>
				<ArtisanCloudLogo/>
			</div>
			<div className={'h-full flex gap-3 ml-auto mr-5'}>
				{isLoggedIn ? (
					<div className={"mt-6"}>
						<Dropdown placement="bottom-end">
							<DropdownTrigger>
								<Avatar style={{
									backgroundColor: '#af99d0',
									verticalAlign: 'middle',
									border: '#A283D2 solid 2px',
								}}
												size="large" gap={4}>
									{user?.account}
								</Avatar>
							</DropdownTrigger>
							<DropdownMenu aria-label="Profile Actions" variant="flat">
								<DropdownItem key="profile" className="h-14 gap-2" textValue="account">
									<p className="font-semibold">{user?.account}</p>
								</DropdownItem>
								<DropdownItem key="space" textValue="工作台">
									<Link href={'space/workspace/robot-chat'}>工作台</Link>
								</DropdownItem>
								<DropdownItem key="logout" onClick={handleLogout} color="danger" textValue="退出">
									退出
								</DropdownItem>
							</DropdownMenu>
						</Dropdown>
					</div>
				) : (
					<>
						<Link href={'/user/register'} className={'text-primary text-md font-bold opacity-65'}>注册</Link>
						<Link href={'/user/login'} className={'text-primary text-md font-bold opacity-65 hover:text-foreground'}>登录</Link>
					</>
				)}
			</div>
		</div>
	);
}
