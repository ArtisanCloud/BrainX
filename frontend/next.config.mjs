import path from 'path';
const __dirname = new URL('.', import.meta.url).pathname;


/** @type {import('next').NextConfig} */
const nextConfig = {
	sassOptions: {
		includePaths: [path.join(__dirname, 'styles')],
	},
	// ssr: false,
	images: {
		remotePatterns: [
			{
				protocol: 'http',
				hostname: '**',
				port: '9001',
				pathname: '**',
			},
			{
				protocol: 'https',
				hostname: '**',
				port: '9001',
				pathname: '**',
			},
		],
	},
	// Develop mode only
	// reactStrictMode: false,
};

export default nextConfig;
