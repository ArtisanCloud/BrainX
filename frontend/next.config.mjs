import path from 'path';

const __dirname = new URL('.', import.meta.url).pathname;


/** @type {import('next').NextConfig} */
const nextConfig = {
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
  // solve nextjs preload google font issue
  experimental: {
    optimizeCss: true,
  },
  // ssr: false,
  images: {
    remotePatterns: [
      {
        // 匹配所有域名
        protocol: 'https',
        hostname: '**',
        port: '',
      },
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
