import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PressW Recipe Chat",
  description: "LLM-powered cooking & recipe Q&A",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
