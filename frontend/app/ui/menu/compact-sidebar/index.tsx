"use client";

import Image from "next/image";
import MenuLink from "@/app/ui/menu/menu-link";
import styles from "./index.module.scss";
import {Button} from "antd"
import {menuItems} from "@/app/ui/menu";
import {LogoutOutlined} from '@ant-design/icons'
import {MdOutlineArrowForward} from "react-icons/md";
import React, {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/ui/menu/provider/sidebar-provider";
import Link from "next/link";
import {useRouter} from "next/navigation";
import Cookies from "js-cookie";
import {token_key} from "@/app/utils/auth";

const CompactSidebar = () => {
	// const { user } = await auth();
	const router = useRouter();
	const {hideSidebar, setHideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
	const handleClickDrawerHandle = () => {
		setHideSidebar(!hideSidebar)
		// console.log(hideSidebar)
	}


	const handleSignOut = (event: any) => {
		event.preventDefault();
		// Your form submission logic here
		Cookies.set(token_key, '', {expires: -1});
		router.push('/')
	}

	return (
		<div className={styles.container}>
			<div className={styles.menu}>
				<div className={styles.user}>
					<Link href={"/"}>
						<Image
							className={styles.userImage}
							src={"/images/logo-s.png"}
							alt=""
							width="50"
							height="50"
						/>
					</Link>
				</div>
				<ul className={styles.list}>
					{menuItems.map((cat) => (
						<li key={cat.title}>
							{cat.list.map((item) => (
								<MenuLink item={item} key={item.title}/>
							))}
						</li>
					))}
				</ul>

				<Button
					onClick={handleSignOut}
					size="small"
					icon={<LogoutOutlined/>}
					className={styles.logout}
				/>
			</div>
			<div className={styles.drawerHandler}>
				<MdOutlineArrowForward onClick={handleClickDrawerHandle}/>
			</div>
		</div>
	);
};

export default CompactSidebar;
