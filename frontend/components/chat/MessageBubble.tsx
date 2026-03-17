"use client";

import { cn } from "@/lib/utils";
import type { ChatMessage } from "./types";

interface MessageBubbleProps {
  message: ChatMessage;
  className?: string;
}

export function MessageBubble({ message, className }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex w-full animate-in fade-in-0 slide-in-from-bottom-2 duration-300",
        isUser ? "justify-end" : "justify-start",
        className
      )}
    >
      <div
        className={cn(
          "max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm",
          isUser
            ? "bg-amber-600 text-white rounded-br-md"
            : "bg-stone-100 text-stone-900 dark:bg-stone-800 dark:text-stone-100 rounded-bl-md"
        )}
      >
        {message.isRefusal && (
          <span className="mb-1 block text-xs font-medium opacity-80">
            Out of scope
          </span>
        )}
        <div className="whitespace-pre-wrap break-words">{message.content}</div>
      </div>
    </div>
  );
}
