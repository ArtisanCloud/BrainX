"use client";

import Image from "next/image";
import MenuLink from "@/app/components/menu/menu-link";
import styles from "./index.module.scss";
import {MdOutlineArrowBack} from "react-icons/md";
import {LogoutOutlined} from '@ant-design/icons'

import {Form} from "antd"
import { menuItems} from "@/app/components/menu";
import React, {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/components/menu/provider/sidebar-provider";
import Link from "next/link";
import {useRouter} from "next/navigation";
import Cookies from "js-cookie";
import {token_key} from "@/app/utils/auth";


const Sidebar = () => {
	// const { user } = await auth();
	const {hideSidebar, setHideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
	const handleClickDrawerHandle = () => {
		setHideSidebar(!hideSidebar)
	}

	const router = useRouter();

	const handleSignOut = (event: any) => {
		event.preventDefault();
		// Your form submission logic here
		Cookies.set(token_key, '', {expires: -1});
		router.push('/')
	}

	return (
		<div className={styles.container}>
			<div className={styles.menu}>
				<Link
					href="/"
				>
					<div className={styles.user}>
						<Image
							className={styles.userImage}
							// src={user.img || "/noavatar.png"}
							src={"/images/logo-s.png"}
							alt=""
							width="50"
							height="50"
						/>
						<div className={styles.userDetail}>
							{/*<span className={styles.username}>{user.username}</span>*/}
							<span className={styles.userTitle}>BrainX</span>
						</div>
					</div>
				</Link>
				<ul className={styles.list}>
					{menuItems.map((cat) => (
						<li key={cat.title}>
							<span className={styles.cat}>{cat.title}</span>
							{cat.list.map((item) => (
								<MenuLink item={item} key={item.title}/>
							))}
						</li>
					))}
				</ul>
				<Form
					name="signout"
					onFinish={handleSignOut}
				>
					<button className={styles.logout}>
						<LogoutOutlined/> Logout
					</button>
				</Form>
			</div>
			<div className={styles.drawerHandler}>
				<MdOutlineArrowBack onClick={handleClickDrawerHandle}/>
			</div>

		</div>
	);
};

export default Sidebar;
