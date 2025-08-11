import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Tip Calculator - Calculate Tips & Split Bills Easily",
  description: "Calculate tips and split bills effortlessly with customizable percentages. Perfect for restaurant goers and travelers. Mobile-friendly and easy to use.",
  keywords: "tip calculator, bill splitter, restaurant tip, gratuity calculator, tip percentage",
  authors: [{ name: "Tip Calculator App" }],
  robots: "index, follow",
  openGraph: {
    title: "Tip Calculator - Calculate Tips & Split Bills Easily",
    description: "Calculate tips and split bills effortlessly with customizable percentages. Perfect for restaurant goers and travelers.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Tip Calculator - Calculate Tips & Split Bills Easily",
    description: "Calculate tips and split bills effortlessly with customizable percentages. Perfect for restaurant goers and travelers.",
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
