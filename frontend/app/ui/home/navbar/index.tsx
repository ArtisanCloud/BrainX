"use client";

import styles from "@/app/ui/home/navbar/index.module.scss";
import ArtisanCloudLogo from "@/app/ui/home/logo/index"
import React from "react";



export default function HomeNavbar() {
	return (
		<div className={styles.container}>
			<div className={styles.headerLeft}>
				<ArtisanCloudLogo/>
			</div>

			<div className={styles.headerRight}>
				<div>user</div>
			</div>
		</div>
	);


}
