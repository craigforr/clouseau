// App-wide state context for selection management

import { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface AppContextValue {
  selectedSessionId: string | null;
  selectedConversationId: string | null;
  selectSession: (sessionId: string | null) => void;
  selectConversation: (conversationId: string | null) => void;
}

const AppContext = createContext<AppContextValue | undefined>(undefined);

interface AppProviderProps {
  children: ReactNode;
}

export function AppProvider({ children }: AppProviderProps) {
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);

  const selectSession = useCallback((sessionId: string | null) => {
    setSelectedSessionId(sessionId);
    // Clear conversation selection when session changes
    setSelectedConversationId(null);
  }, []);

  const selectConversation = useCallback((conversationId: string | null) => {
    setSelectedConversationId(conversationId);
  }, []);

  const value: AppContextValue = {
    selectedSessionId,
    selectedConversationId,
    selectSession,
    selectConversation,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useAppContext(): AppContextValue {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}
