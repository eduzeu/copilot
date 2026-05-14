import "./globals.css";

export const metadata = {
  title: "Career Copilot",
  description: "AI-powered job search assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}