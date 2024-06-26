"use client"

import Sidebar from "@/app/ui/menu/sidebar";
import CompactSidebar from "@/app/ui/menu/compact-sidebar";
import useWindowSize from "@/app/lib/windows";
import {MdDashboard, MdHelpCenter, MdOutlineSettings, MdPeople, MdSupervisedUserCircle} from "react-icons/md";
import {HiOutlineAcademicCap} from "react-icons/hi";
import {RiRobot2Line} from "react-icons/ri";
import {GrAppsRounded, GrBusinessService} from "react-icons/gr";
import React, {useContext, useEffect} from "react";
import SidebarProvider, {HideSidebarContext, SidebarContextType} from "@/app/ui/menu/provider/sidebar-provider";

export const menuItems = [

	{
		title: "工作区",
		list: [
			{
				title: "智能助理",
				path: "/space/workspace/robot-chat",
				icon: <RiRobot2Line/>,
			},
			{
				title: "智能问答",
				path: "/space/workspace/question-answer",
				icon: <HiOutlineAcademicCap/>,
			},

		]
	},
	{
		title: "应用",
		list: [
			{
				title: "我的应用",
				path: "/space/app/mine",
				icon: <GrAppsRounded/>,
				defaultParams: {pathname: '/space/app/mine/app'}
			},
			{
				title: "应用市场",
				path: "/space/app/market",
				icon: <GrBusinessService/>,
			},
		],
	},
	{
		title: "分析",
		list: [
			{
				title: "仪表盘",
				path: "/space/dashboard",
				icon: <MdDashboard/>,
			},
		],
	},
	{
		title: "协作",
		list: [

			{
				title: "用户",
				path: "/space/users",
				icon: <MdSupervisedUserCircle/>,
			},
			{
				title: "团队",
				path: "/space/teams",
				icon: <MdPeople/>,
			},
		],
	},
	{
		title: "其他",
		list: [
			{
				title: "设置",
				path: "/space/settings",
				icon: <MdOutlineSettings/>,
			},
			{
				title: "帮助",
				path: "/space/help",
				icon: <MdHelpCenter/>,
			},
		],
	},
];

export const handleSignOut = (event: any) => {
	event.preventDefault();
	// Your form submission logic here
	// await signOut();
}

const Menu = () => {
	const {width} = useWindowSize();
	const {hideSidebar} = useContext(HideSidebarContext) as SidebarContextType;

	return (
		<div>
			{/*{width > 1024 ? (*/}
			{!hideSidebar ? (
				<Sidebar/>
			) : (
				<CompactSidebar/>
			)}
		</div>
	)
}
export default Menu
