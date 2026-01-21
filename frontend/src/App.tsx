import { AppProvider } from './context/AppContext';
import SessionBrowser from './components/SessionBrowser/SessionBrowser';
import Chat from './components/Chat/Chat';

function AppContent() {
  return (
    <div className="min-h-screen h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
      <header className="bg-white dark:bg-gray-800 shadow-sm shrink-0">
        <div className="px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Clouseau
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            LLM Interaction Inspector
          </p>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-hidden">
          <SessionBrowser />
        </aside>

        {/* Main content */}
        <main className="flex-1 bg-white dark:bg-gray-800 overflow-hidden">
          <Chat />
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
