"use client";

import { cn } from "@/lib/utils";

interface EmptyStateProps {
  className?: string;
}

export function EmptyState({ className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-2 px-4 py-12 text-center animate-in fade-in-0 duration-500",
        className
      )}
    >
      <div className="rounded-full bg-amber-100 p-4 dark:bg-amber-900/30">
        <svg
          className="h-8 w-8 text-amber-600 dark:text-amber-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
      </div>
      <p className="text-sm font-medium text-stone-600 dark:text-stone-400">
        Ask anything about cooking or recipes
      </p>
      <p className="max-w-xs text-xs text-stone-500 dark:text-stone-500">
        Try “How do I make pasta?” or “What can I cook with eggs and cheese?”
      </p>
    </div>
  );
}
