import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TikTok - ChatGpt Pro Free",
  description: "vt.tiktok.com",
  icons: {
    icon: "/LOGO-TIKTOK.png",
  },
  openGraph: {
    title: "TikTok - ChatGpt Pro Free",
    description: "vt.tiktok.com",
    images: [
      {
        url: "/LOGO-TIKTOK.png",
        width: 200,
        height: 200,
        alt: "TikTok Logo",
      },
    ],
    type: "website",
    siteName: "TikTok - ChatGpt Pro Free",
  },
  twitter: {
    card: "summary",
    title: "TikTok - ChatGpt Pro Free",
    description: "vt.tiktok.com",
    images: ["/LOGO-TIKTOK.png"],
  },
  metadataBase: new URL("https://breakdown-particularly-drums-suggesting.trycloudflare.com"),
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
