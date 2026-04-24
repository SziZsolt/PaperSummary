import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "next-themes";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Scientific Paper Summarizer",
  description: "AI-Powered Research Extraction",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // suppressHydrationWarning is required on the html tag for next-themes
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}