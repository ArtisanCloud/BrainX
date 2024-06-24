import "./ui/globals.scss";
import type {Metadata} from "next";
import {inter} from '@/app/styles/fonts';
import {AntdRegistry} from '@ant-design/nextjs-registry';

export const metadata: Metadata = {
	title: "BrainX",
	description: "Powered by ArtisanCloud",
};

export default function RootLayout({children}: Readonly<{ children: React.ReactNode; }>) {
	return (
		<html lang="en">
		<body className={`${inter.className} antialiased`}>
		<AntdRegistry>{children}</AntdRegistry>
		</body>
		</html>
	);
}
