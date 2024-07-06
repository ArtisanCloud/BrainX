"use client";

import Image from "next/image";
import MenuLink from "@/app/ui/menu/menu-link";
import styles from "./index.module.scss";
import {Button} from "antd"
import {handleSignOut, menuItems} from "@/app/ui/menu";
import {LogoutOutlined} from '@ant-design/icons'
import {MdOutlineArrowForward} from "react-icons/md";
import React, {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/ui/menu/provider/sidebar-provider";

const CompactSidebar = () => {
	// const { user } = await auth();
	const {hideSidebar, setHideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
	const handleClickDrawerHandle = () => {
		setHideSidebar(!hideSidebar)
		// console.log(hideSidebar)
	}

	return (
		<div className={styles.container}>
			<div className={styles.menu}>
				<div className={styles.user}>
					<Image
						className={styles.userImage}
						// src={user.img || "/noavatar.png"}
						src={"/images/logo-s.png"}
						alt=""
						width="50"
						height="50"
					/>
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
