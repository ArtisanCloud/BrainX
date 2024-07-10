"use client";
import ArtisanCloudLogo from "@/app/ui/home/logo/index"
import React from "react";
import {
	Link,
} from "@nextui-org/react";


export default function HomeNavbar() {
	return (
		<div className={'h-24  bg-gradient-to-b-header  bg-bottom-100 bg-100x200 transition-all duration-500 w-full flex items-center px-7'}>
			<div className={'opacity-80'}>
				<ArtisanCloudLogo/>
			</div>
			<div className={'h-full flex gap-3 ml-auto mr-5'}>
				<Link href={'/'} className={'text-primary text-md font-bold opacity-65'}>首页</Link>
				<Link href={'/user/register'} className={'text-primary text-md font-bold opacity-65'}>注册</Link>
				<Link href={'/auth/login'} className={'text-primary text-md font-bold opacity-65 hover:text-foreground'}>登陆</Link>
			</div>
		</div>
	);
}
