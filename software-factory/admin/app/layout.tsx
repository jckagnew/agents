import type { ReactNode } from "react";
import "./globals.css";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <aside className="sidebar">
            <div className="brand">Factory Admin</div>
            <nav>
              <a href="/" className="nav-link">Dashboard</a>
              <a href="/projects" className="nav-link">Projects</a>
              <a href="/health" className="nav-link">Health Alerts</a>
              <a href="/splash" className="nav-link">Splash Creator</a>
            </nav>
          </aside>
          <main className="content">{children}</main>
        </div>
        <style jsx global>{`
          .app-shell {
            display: grid;
            grid-template-columns: 260px 1fr;
            min-height: 100vh;
          }

          .sidebar {
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
            color: #f9fafb;
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
          }

          .brand {
            font-size: 1.4rem;
            font-weight: 600;
          }

          nav {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
          }

          .nav-link {
            color: rgba(249, 250, 251, 0.75);
            text-decoration: none;
            font-weight: 500;
          }

          .nav-link:hover,
          .nav-link:focus {
            color: #ffffff;
          }

          .content {
            padding: 3rem;
          }

          @media (max-width: 960px) {
            .app-shell {
              grid-template-columns: 1fr;
            }

            .sidebar {
              flex-direction: row;
              justify-content: space-between;
              align-items: center;
            }

            nav {
              flex-direction: row;
              gap: 1rem;
            }
          }
        `}</style>
      </body>
    </html>
  );
}
