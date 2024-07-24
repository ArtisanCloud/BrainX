"use client";
import {usePathname} from "next/navigation";
import styles from "./index.module.scss";
import Link from 'next/link'
import {useContext, useEffect, useState} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/components/menu/provider/sidebar-provider";
import useWindowSize from "@/app/lib/windows";

const links = [

	{
		key: "app",
		label: "机器人",
		link: "/space/app"
	},
	{
		key: "knowledge",
		label: "知识库",
		link: "/space/knowledge"
	},
	{
		key: "workflow",
		label: "工作流",
		link: "/space/workflow"
	},
	{
		key: "plugins",
		label: "插件",
		link: "/space/plugins"
	}
]

const Navbar = () => {
	const pathname = usePathname();

	const {hideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
	const {width} = useWindowSize();

	useEffect(() => {
		const navbar = document.getElementById('navbar')
		// console.log(width)
		const menuWidth = 200
		const compactMenuWidth = 50
		let newWidth = width - compactMenuWidth;
		if (navbar) {
			if (!hideSidebar) {
				newWidth = width - menuWidth;
			}
			navbar.style.width = `${newWidth}px`;
			// console.log(navbar.style.width)
		}
	}, [hideSidebar, width]);

	return (
		<div className={styles.container} id='navbar'>
			<div className={styles.title}>{pathname.split("/").pop()}</div>
			<div className={styles.menu}>
				{
					links.map((link) => (
						<Link
							key={link.key}
							href={link.link}
							className={`${styles.link} ${pathname === link.link ? styles.active : ''}`}
						>{link.label}</Link>
					))
				}
			</div>
		</div>
	);
};

export default Navbar;
