"use client";

import styles from "@/app/ui/home/navbar/index.module.scss";
import ArtisanCloudLogo from "@/app/ui/home/logo/index"
import React from "react";
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button, DropdownItem, DropdownTrigger, Dropdown, DropdownMenu} from "@nextui-org/react";


export default function HomeNavbar() {
	return (
		<div className={styles.container}>
			<Navbar>
				<NavbarBrand>
					<ArtisanCloudLogo />
				</NavbarBrand>
				<NavbarContent className="hidden sm:flex gap-4" justify="center">
					{/*<Dropdown>*/}
					{/*	<NavbarItem>*/}
					{/*		<DropdownTrigger>*/}
					{/*			<Button*/}
					{/*				disableRipple*/}
					{/*				className="p-0 bg-transparent data-[hover=true]:bg-transparent"*/}
					{/*				// endContent={icons.chevron}*/}
					{/*				radius="sm"*/}
					{/*				variant="light"*/}
					{/*			>*/}
					{/*				Features*/}
					{/*			</Button>*/}
					{/*		</DropdownTrigger>*/}
					{/*	</NavbarItem>*/}
					{/*	<DropdownMenu*/}
					{/*		aria-label="ACME features"*/}
					{/*		className="w-[340px]"*/}
					{/*		itemClasses={{*/}
					{/*			base: "gap-4",*/}
					{/*		}}*/}
					{/*	>*/}
					{/*		<DropdownItem*/}
					{/*			key="autoscaling"*/}
					{/*			description="ACME scales apps to meet user demand, automagically, based on load."*/}
					{/*			// startContent={icons.scale}*/}
					{/*		>*/}
					{/*			Autoscaling*/}
					{/*		</DropdownItem>*/}
					{/*		<DropdownItem*/}
					{/*			key="usage_metrics"*/}
					{/*			description="Real-time metrics to debug issues. Slow query added? We’ll show you exactly where."*/}
					{/*			// startContent={icons.activity}*/}
					{/*		>*/}
					{/*			Usage Metrics*/}
					{/*		</DropdownItem>*/}
					{/*		<DropdownItem*/}
					{/*			key="production_ready"*/}
					{/*			description="ACME runs on ACME, join us and others serving requests at web scale."*/}
					{/*			// startContent={icons.flash}*/}
					{/*		>*/}
					{/*			Production Ready*/}
					{/*		</DropdownItem>*/}
					{/*		<DropdownItem*/}
					{/*			key="99_uptime"*/}
					{/*			description="Applications stay on the grid with high availability and high uptime guarantees."*/}
					{/*			// startContent={icons.server}*/}
					{/*		>*/}
					{/*			+99% Uptime*/}
					{/*		</DropdownItem>*/}
					{/*		<DropdownItem*/}
					{/*			key="supreme_support"*/}
					{/*			description="Overcome any challenge with a supporting team ready to respond."*/}
					{/*			// startContent={icons.user}*/}
					{/*		>*/}
					{/*			+Supreme Support*/}
					{/*		</DropdownItem>*/}
					{/*	</DropdownMenu>*/}
					{/*</Dropdown>*/}
					<NavbarItem isActive>
						<Link href="#" aria-current="page">
							产品
						</Link>
					</NavbarItem>
					<NavbarItem>
						<Link color="foreground" href="#">
							文档
						</Link>
					</NavbarItem>
				</NavbarContent>
				<NavbarContent justify="end">
					<NavbarItem className="hidden lg:flex">
						<Link href="#">登陆</Link>
					</NavbarItem>
					<NavbarItem>
						<Button as={Link} color="primary" href="#" variant="flat">
							注册
						</Button>
					</NavbarItem>
				</NavbarContent>
			</Navbar>
		</div>
	);


}
