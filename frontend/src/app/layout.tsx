import type { Metadata } from 'next';
import { AuthProvider } from '@/hooks/useAuth';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title:       "GlobalNet'I — Sistema de Gestão",
  description: 'Sistema de gestão financeira para provedores de internet',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
