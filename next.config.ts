import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'books.google.com',
        port: '',
        pathname: '/books/content/**',
      },
      // You can add other trusted domains here as needed,
      // for example, if some covers use 'https':
      {
        protocol: 'https',
        hostname: 'books.google.com',
        port: '',
        pathname: '/books/content/**',
      }
    ],
  },
};

export default nextConfig;
