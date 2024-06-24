import { BeakerIcon } from '@heroicons/react/24/outline';
import { noto_serif } from '@/app/styles/fonts';
import React from "react";
import Image from "next/image";
import styles from "@/app/ui/home/logo/index.module.scss";

export default function Index() {
	return (
		<div
			className={styles.container}
		>
			{/*<BeakerIcon className="h-12 w-12" />*/}
			<Image
				className={styles.logo}
				src="/logo-s.png"
				width={48} height={48}
				priority={true}
				alt="artisan cloud present logo"
			/>
			<p className={styles.brand}>BrainX</p>
		</div>
	);
}