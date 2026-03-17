"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

export function ChatInput({
  onSend,
  disabled,
  placeholder = "Ask about recipes, ingredients, or cooking...",
  className,
}: ChatInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`;
  }, [value]);

  return (
    <div
      className={cn(
        "flex gap-2 rounded-xl border border-stone-200 bg-white p-2 shadow-sm transition-shadow focus-within:ring-2 focus-within:ring-amber-500/20 dark:border-stone-700 dark:bg-stone-900",
        className
      )}
    >
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
        className="min-h-[40px] max-h-40 flex-1 resize-none rounded-lg bg-transparent px-3 py-2 text-sm outline-none placeholder:text-stone-400 disabled:opacity-50 dark:placeholder:text-stone-500"
      />
      <Button
        type="button"
        onClick={handleSubmit}
        disabled={disabled || !value.trim()}
        className="self-end shrink-0 transition-transform hover:scale-[1.02] active:scale-[0.98]"
      >
        Send
      </Button>
    </div>
  );
}
