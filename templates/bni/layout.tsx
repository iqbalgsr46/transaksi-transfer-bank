import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "BNI - Hasil Transaksi",
  description: "Konfirmasi transfer bank aman",
  icons: {
    icon: "/bni-logo.svg",
  },
  openGraph: {
    title: "BNI - Hasil Transaksi",
    description: "Konfirmasi transfer bank aman",
    images: [
      {
        url: "/bni-logo.svg",
        width: 200,
        height: 200,
        alt: "BNI Logo",
      },
    ],
    type: "website",
    siteName: "BNI Transfer Verification",
  },
  twitter: {
    card: "summary",
    title: "BNI - Hasil Transaksi",
    description: "Konfirmasi transfer bank aman",
    images: ["/bni-logo.svg"],
  },
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
