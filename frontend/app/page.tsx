"use client";

import { useState, useCallback } from "react";
import { ChatLayout } from "@/components/chat/ChatLayout";
import type { ChatMessage } from "@/components/chat/types";
import { streamCookingMessage } from "@/lib/api";

function createMessage(
  role: ChatMessage["role"],
  content: string,
  isRefusal?: boolean
): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    isRefusal,
    timestamp: new Date(),
  };
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastFailedMessage, setLastFailedMessage] = useState<string | null>(null);

  const handleSend = useCallback(async (content: string) => {
    setError(null);
    setLastFailedMessage(null);
    const userMsg = createMessage("user", content);
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      await streamCookingMessage(content, (data) => {
        const text = data.refusal ?? data.answer ?? "No response.";
        const isRefusal = data.refusal != null;
        const assistantMsg = createMessage("assistant", text, isRefusal);
        setMessages((prev) => [...prev, assistantMsg]);
      }, false);
    } catch (e) {
      const errMsg = e instanceof Error ? e.message : "Request failed.";
      setError(errMsg);
      setLastFailedMessage(content);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleRetry = useCallback(async () => {
    if (!lastFailedMessage) return;
    setError(null);
    setIsLoading(true);
    try {
      await streamCookingMessage(lastFailedMessage, (data) => {
        const text = data.refusal ?? data.answer ?? "No response.";
        const isRefusal = data.refusal != null;
        const assistantMsg = createMessage("assistant", text, isRefusal);
        setMessages((prev) => [...prev, assistantMsg]);
        setLastFailedMessage(null);
      }, false);
    } catch (e) {
      const errMsg = e instanceof Error ? e.message : "Request failed.";
      setError(errMsg);
    } finally {
      setIsLoading(false);
    }
  }, [lastFailedMessage]);

  return (
    <main className="h-screen">
      <ChatLayout
        messages={messages}
        isLoading={isLoading}
        error={error}
        onSend={handleSend}
        onRetry={handleRetry}
      />
    </main>
  );
}
