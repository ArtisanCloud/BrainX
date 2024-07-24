"use client"

import Link from 'next/link'
import styles from './index.module.scss'
import {usePathname} from 'next/navigation'
import useWindowSize from "@/app/lib/windows";
import {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/components/menu/provider/sidebar-provider";

const Index = ({item}: any) => {
	const {width} = useWindowSize();
	const pathname = usePathname()
	const {hideSidebar} = useContext(HideSidebarContext) as SidebarContextType;

	return (
		<Link
			href={{
				pathname: item.path,
				...item.defaultParams
			}}
			className={`${!hideSidebar ? styles.container : styles.containerCompact} 
			${pathname.match(new RegExp(`^${item.path}`)) && styles.active}`}
		>
		<div className={styles.icon}>{item.icon}</div>
			{/*{width > 1024 ? item.title : ""}*/}
			{!hideSidebar ? item.title : ""}
		</Link>
	)
}

export default Index
