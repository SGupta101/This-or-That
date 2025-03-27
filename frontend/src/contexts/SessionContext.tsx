import { createContext, useContext } from 'react';

const SessionContext = createContext<string | null>(null);

export const SessionProvider = ({ children, sessionId }: { children: React.ReactNode; sessionId: string | null }) => {
  return <SessionContext.Provider value={sessionId}>{children}</SessionContext.Provider>;
};

export const useSessionId = () => {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSessionId must be used within a SessionProvider');
  }
  return context;
};
