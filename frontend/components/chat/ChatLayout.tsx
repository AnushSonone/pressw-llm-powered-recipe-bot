"use client";

import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import type { ChatMessage } from "./types";

interface ChatLayoutProps {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  onSend: (message: string) => void;
  onRetry: () => void;
}

export function ChatLayout({
  messages,
  isLoading,
  error,
  onSend,
  onRetry,
}: ChatLayoutProps) {
  return (
    <div className="flex h-screen flex-col">
      <header className="shrink-0 border-b border-stone-200 bg-white/80 px-4 py-3 backdrop-blur-sm dark:border-stone-800 dark:bg-stone-900/80">
        <h1 className="text-lg font-semibold tracking-tight text-stone-900 dark:text-stone-100">
          PressW Recipe Chat
        </h1>
        <p className="text-xs text-stone-500 dark:text-stone-400">
          Ask about recipes, ingredients, or cooking—I’ll check what you can make
          with your tools.
        </p>
      </header>

      <div className="min-h-0 flex-1">
        <MessageList
          messages={messages}
          isLoading={isLoading}
          error={error}
          onRetry={onRetry}
          className="h-full"
        />
      </div>

      <div className="shrink-0 border-t border-stone-200 bg-white/80 px-4 py-3 backdrop-blur-sm dark:border-stone-800 dark:bg-stone-900/80">
        <ChatInput onSend={onSend} disabled={isLoading} />
      </div>
    </div>
  );
}
