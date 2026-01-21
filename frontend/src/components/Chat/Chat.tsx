import { useExchanges } from '../../hooks';
import { useAppContext } from '../../context/AppContext';
import { formatDate } from '../../utils';
import type { Exchange } from '../../types';

function TokenMetadata({ exchange }: { exchange: Exchange }) {
  if (!exchange.model && !exchange.inputTokens && !exchange.outputTokens) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 text-xs text-gray-400 dark:text-gray-500 mt-1">
      {exchange.model && <span className="font-mono">{exchange.model}</span>}
      {(exchange.inputTokens || exchange.outputTokens) && (
        <span>
          {exchange.inputTokens ?? 0} in / {exchange.outputTokens ?? 0} out tokens
        </span>
      )}
    </div>
  );
}

function ExchangeBubble({ exchange }: { exchange: Exchange }) {
  return (
    <div className="space-y-4 mb-6">
      {/* User message - right aligned */}
      <div className="flex justify-end">
        <div className="max-w-[80%]">
          <div className="bg-blue-500 text-white rounded-lg rounded-br-sm px-4 py-2 shadow-sm">
            <div className="whitespace-pre-wrap break-words">{exchange.userMessage}</div>
          </div>
          <div className="text-xs text-gray-400 dark:text-gray-500 mt-1 text-right">
            {formatDate(exchange.createdAt)}
          </div>
        </div>
      </div>

      {/* Assistant message - left aligned */}
      <div className="flex justify-start">
        <div className="max-w-[80%]">
          <div className="bg-gray-100 dark:bg-gray-700 rounded-lg rounded-bl-sm px-4 py-2 shadow-sm">
            <div className="whitespace-pre-wrap break-words text-gray-900 dark:text-gray-100">
              {exchange.assistantMessage}
            </div>
          </div>
          <TokenMetadata exchange={exchange} />
        </div>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="h-full flex items-center justify-center">
      <div className="text-center text-gray-500 dark:text-gray-400">
        <svg
          className="mx-auto h-12 w-12 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
        <p className="text-lg font-medium">No conversation selected</p>
        <p className="text-sm mt-1">Select a conversation from the sidebar to view exchanges</p>
      </div>
    </div>
  );
}

function Chat() {
  const { selectedConversationId } = useAppContext();
  const { exchanges, loading, error } = useExchanges(selectedConversationId);

  if (!selectedConversationId) {
    return (
      <div className="chat-container h-full">
        <EmptyState />
      </div>
    );
  }

  return (
    <div className="chat-container h-full flex flex-col">
      <div className="flex-1 overflow-y-auto p-6">
        {loading && (
          <div className="flex items-center justify-center h-full">
            <div className="text-gray-500 dark:text-gray-400">Loading exchanges...</div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-full">
            <div className="text-red-500 dark:text-red-400">Error: {error.message}</div>
          </div>
        )}

        {!loading && !error && exchanges.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-gray-500 dark:text-gray-400">No exchanges in this conversation</div>
          </div>
        )}

        {!loading && !error && exchanges.length > 0 && (
          <div>
            {exchanges.map((exchange) => (
              <ExchangeBubble key={exchange.id} exchange={exchange} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;
