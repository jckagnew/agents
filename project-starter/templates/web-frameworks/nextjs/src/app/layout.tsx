import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "{{PROJECT_NAME}}",
  description: "{{PROJECT_DESCRIPTION}}",
  keywords: ["{{KEYWORDS}}"],
  authors: [{ name: "{{AUTHOR_NAME}}", url: "{{AUTHOR_URL}}" }],
  creator: "{{AUTHOR_NAME}}",
  publisher: "{{AUTHOR_NAME}}",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("{{BASE_URL}}"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "{{PROJECT_NAME}}",
    description: "{{PROJECT_DESCRIPTION}}",
    url: "{{BASE_URL}}",
    siteName: "{{PROJECT_NAME}}",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "{{PROJECT_NAME}}",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "{{PROJECT_NAME}}",
    description: "{{PROJECT_DESCRIPTION}}",
    images: ["/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="min-h-screen bg-background font-sans antialiased">
          {children}
        </div>
      </body>
    </html>
  );
}
