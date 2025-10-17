import type { CSSProperties, ReactNode } from "react";
import type { Metadata } from "next";
import { Nunito, Poppins } from "next/font/google";
import "./globals.css";
import {
  colors,
  typography,
  spacing,
  borderRadius,
} from "../../../../../design-system/googleTheme";

const poppins = Poppins({
  subsets: ["latin"],
  variable: "--font-poppins",
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const toKebabCase = (value: string) =>
  value.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();

const createThemeCustomProperties = (): CSSProperties => {
  const customProperties: Record<string, string> = {};

  Object.entries(colors).forEach(([token, value]) => {
    customProperties[`--color-${toKebabCase(token)}`] = value;
  });

  Object.entries(spacing).forEach(([token, value]) => {
    customProperties[`--spacing-${toKebabCase(token)}`] = `${value}px`;
  });

  Object.entries(borderRadius).forEach(([token, value]) => {
    customProperties[`--radius-${toKebabCase(token)}`] = `${value}px`;
  });

  Object.entries(typography.fontSize).forEach(([token, value]) => {
    customProperties[`--font-size-${toKebabCase(token)}`] = `${value}px`;
  });

  Object.entries(typography.lineHeight).forEach(([token, value]) => {
    customProperties[`--line-height-${toKebabCase(token)}`] = String(value);
  });

  Object.entries(typography.letterSpacing).forEach(([token, value]) => {
    customProperties[`--letter-spacing-${toKebabCase(token)}`] = `${value}px`;
  });

  customProperties["--font-heading"] =
    "var(--font-poppins, 'Poppins', 'Helvetica Neue', sans-serif)";
  customProperties["--font-body"] =
    "var(--font-nunito, 'Nunito', 'Helvetica Neue', sans-serif)";
  customProperties["--font-body-medium"] =
    "var(--font-nunito, 'Nunito', 'Helvetica Neue', sans-serif)";
  customProperties["--font-label"] =
    "var(--font-nunito, 'Nunito', 'Helvetica Neue', sans-serif)";

  return customProperties as CSSProperties;
};

const themeCustomProperties = createThemeCustomProperties();

const bodyStyle: CSSProperties = {
  ...themeCustomProperties,
  backgroundColor: colors.background,
  color: colors.textPrimary,
  fontFamily: "var(--font-body, 'Nunito', 'Helvetica Neue', sans-serif)",
  lineHeight: "var(--line-height-normal, 1.4)",
};

export const metadata: Metadata = {
  title: "Weight Tracker Pro",
  description:
    "Cross-platform weight tracking dashboard aligned with shared design tokens.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${poppins.variable} ${nunito.variable} antialiased`}
        style={bodyStyle}
      >
        {children}
      </body>
    </html>
  );
}
