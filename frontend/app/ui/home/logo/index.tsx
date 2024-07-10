import {BeakerIcon} from '@heroicons/react/24/outline';
import {noto_serif} from '@/app/styles/fonts';
import React from "react";
import Image from "next/image";
import styles from "@/app/ui/home/logo/index.module.scss";
import Link from "next/link";

export default function Index() {
	return (
		<div
			className={styles.container}
		>
			<Link href={"/"}>
				<Image
					className={styles.logo}
					src="/images/logo-s.png"
					width={48} height={48}
					priority={true}
					alt="artisan cloud present logo"
				/>
			</Link>
			<p className={styles.brand}>BrainX</p>
		</div>
	);
}
