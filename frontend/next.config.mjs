import path from 'path';
const __dirname = new URL('.', import.meta.url).pathname;


/** @type {import('next').NextConfig} */
const nextConfig = {
	sassOptions: {
		includePaths: [path.join(__dirname, 'styles')],
	},
};

export default nextConfig;
