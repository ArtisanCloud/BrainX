import Link from 'next/link';
import {ArrowRightIcon} from '@heroicons/react/24/outline';
import styles from '@/app/ui/home/home.module.scss';
import HomeNavbar from "@/app/ui/home/navbar";
import brainxImage from '/public/images/brainx.jpeg';
import {Button, Image} from "@nextui-org/react"

export default function Home() {
	return (
		<main className={`${styles.container}`}>
			<HomeNavbar/>
			<div className={'flex h-content bg-bodyDefault w-screen'}>
				<div className={'w-2/3 h-full flex flex-col justify-center pl-10'}>
					<p className={'text-xl font-bold mb-0.5'}>欢迎使用BrainX.</p>
					<p className={'text-4xl font-bold'}>BrainX是一个基于ArtisanCloud的应用程序.</p>
					<div className={'mt-3'}>
						<Button color={'primary'}  className={'rounded opacity-75'} endContent={<ArrowRightIcon className={'text-white w-10 scale-75'} />}>开始</Button>
					</div>
				</div>
				<div className={'w-1/3 flex justify-center flex-col'}>
					<div className={'relative h-800 w-800 scale-50 -ml-52'}>
						<Image src={brainxImage.src} width={800} height={800} className={'absolute left-0 top-0 z-10 rounded-full'} />
						<div id={'card-item-bg'} style={{
							'--image': `url(${brainxImage.src})`,
							backgroundImage: `var(--image)`,
							backgroundSize: 'cover',
							transition: '0.3s ease-in-out',
						} as React.CSSProperties} className={'absolute w-800 h-800 left-0 top-0 scale-105 soft-card-img hero-gradient blur-lg z-1 rounded-full'} />
					</div>
				</div>
			</div>
			<div className={styles.footer}>
				<span>Powered By ArtisanCloud</span>
			</div>
		</main>
	);
}
