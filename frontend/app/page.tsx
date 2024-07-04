import Link from 'next/link';
import {ArrowRightIcon} from '@heroicons/react/24/outline';
import Image from 'next/image';
import styles from '@/app/ui/home/home.module.scss';
import HomeNavbar from "@/app/ui/home/navbar";

export default function Home() {
	return (
		<main className={styles.container}>
			<HomeNavbar/>
			<div className={styles.body}>
				<div className={styles.containerSlogan}>
					<div
						className={styles.mark}
					/>
					<p className={styles.slogan}>
						<strong>欢迎使用 BrainX.</strong> <br/>这是一个很有意思的网络知识系统，提供智能化系统，欢迎来体验。
					</p>
					<Link
						href="/space/workspace/robot-chat"
						className="flex items-center gap-5 self-start rounded-lg bg-blue-500 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-400 md:text-base"
					>
						<span>开始</span> <ArrowRightIcon className="w-5 md:w-6"/>
					</Link>
				</div>
				<div className={styles.containerLogo}>
					{/* Add Hero Images Here */}
					<Image
						src="/brainx.jpeg"
						width={1000}
						height={760}
						priority={true}
						alt="Screenshots of the dashboard project showing desktop version"
					/>
				</div>
			</div>
			<div className={styles.footer}>
				<span>Powered By ArtisanCloud</span>
			</div>
		</main>
	);
}
