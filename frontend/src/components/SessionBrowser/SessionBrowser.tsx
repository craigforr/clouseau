import { useSessions, useConversations } from '../../hooks';
import { useAppContext } from '../../context/AppContext';
import { formatRelativeDate } from '../../utils';
import type { Session, Conversation } from '../../types';

function SessionItem({
  session,
  isSelected,
  onSelect,
}: {
  session: Session;
  isSelected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      onClick={onSelect}
      className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
        isSelected
          ? 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
          : 'hover:bg-gray-100 dark:hover:bg-gray-700'
      }`}
    >
      <div className="font-medium text-sm truncate">{session.name}</div>
      {session.description && (
        <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
          {session.description}
        </div>
      )}
      <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
        {formatRelativeDate(session.updatedAt)}
      </div>
    </button>
  );
}

function ConversationItem({
  conversation,
  isSelected,
  onSelect,
}: {
  conversation: Conversation;
  isSelected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      onClick={onSelect}
      className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
        isSelected
          ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
          : 'hover:bg-gray-100 dark:hover:bg-gray-700'
      }`}
    >
      <div className="text-sm truncate">{conversation.title}</div>
      <div className="text-xs text-gray-400 dark:text-gray-500">
        {formatRelativeDate(conversation.createdAt)}
      </div>
    </button>
  );
}

function ConversationsList({ sessionId }: { sessionId: string }) {
  const { selectedConversationId, selectConversation } = useAppContext();
  const { conversations, loading, error } = useConversations(sessionId);

  if (loading) {
    return (
      <div className="pl-4 py-2 text-sm text-gray-500 dark:text-gray-400">
        Loading conversations...
      </div>
    );
  }

  if (error) {
    return (
      <div className="pl-4 py-2 text-sm text-red-500 dark:text-red-400">
        Error: {error.message}
      </div>
    );
  }

  if (conversations.length === 0) {
    return (
      <div className="pl-4 py-2 text-sm text-gray-500 dark:text-gray-400">
        No conversations
      </div>
    );
  }

  return (
    <div className="pl-4 space-y-1">
      {conversations.map((conversation) => (
        <ConversationItem
          key={conversation.id}
          conversation={conversation}
          isSelected={selectedConversationId === conversation.id}
          onSelect={() => selectConversation(conversation.id)}
        />
      ))}
    </div>
  );
}

function SessionBrowser() {
  const { selectedSessionId, selectSession } = useAppContext();
  const { sessions, loading, error } = useSessions();

  return (
    <div className="session-browser h-full flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="font-semibold text-gray-900 dark:text-white">Sessions</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {loading && (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400">
            Loading sessions...
          </div>
        )}

        {error && (
          <div className="p-4 text-center text-red-500 dark:text-red-400">
            Error: {error.message}
          </div>
        )}

        {!loading && !error && sessions.length === 0 && (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400">
            No sessions found
          </div>
        )}

        {!loading && !error && sessions.length > 0 && (
          <div className="space-y-1">
            {sessions.map((session) => (
              <div key={session.id}>
                <SessionItem
                  session={session}
                  isSelected={selectedSessionId === session.id}
                  onSelect={() => selectSession(session.id)}
                />
                {selectedSessionId === session.id && (
                  <ConversationsList sessionId={session.id} />
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default SessionBrowser;
