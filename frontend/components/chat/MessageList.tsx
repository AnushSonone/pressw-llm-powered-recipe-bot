"use client";

import { useEffect, useRef } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { MessageBubble } from "./MessageBubble";
import { LoadingIndicator } from "./LoadingIndicator";
import { ErrorState } from "./ErrorState";
import { EmptyState } from "./EmptyState";
import type { ChatMessage } from "./types";

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  error: string | null;
  onRetry?: () => void;
  className?: string;
}

export function MessageList({
  messages,
  isLoading,
  error,
  onRetry,
  className,
}: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const isEmpty = messages.length === 0 && !isLoading && !error;

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, isLoading]);

  return (
    <ScrollArea className={className}>
      {isEmpty ? (
        <EmptyState className="h-full min-h-[200px]" />
      ) : (
        <div className="flex flex-col gap-4 px-2 pb-4 pt-2">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {isLoading && <LoadingIndicator />}
          {error && <ErrorState message={error} onRetry={onRetry} />}
        </div>
      )}
      <div ref={scrollRef} />
    </ScrollArea>
  );
}
