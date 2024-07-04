import "./ui/globals.scss";
import type {Metadata} from "next";
import {inter} from '@/app/styles/fonts';
import {AntdRegistry} from '@ant-design/nextjs-registry';
import {NextUIProvider} from "@nextui-org/react";

export const metadata: Metadata = {
	title: "BrainX",
	description: "Powered by ArtisanCloud",
};

export default function RootLayout({children}: Readonly<{ children: React.ReactNode; }>) {
	return (
		<html lang="en">
		<body className={`${inter.className} antialiased`}>
		<AntdRegistry>
			<NextUIProvider>
				{children}
			</NextUIProvider>
		</AntdRegistry>
		</body>
		</html>
	);
}
