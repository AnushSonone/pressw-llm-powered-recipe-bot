"use client";

import { cn } from "@/lib/utils";

interface LoadingIndicatorProps {
  className?: string;
}

export function LoadingIndicator({ className }: LoadingIndicatorProps) {
  return (
    <div
      className={cn(
        "flex justify-start animate-in fade-in-0 duration-200",
        className
      )}
    >
      <div className="rounded-2xl rounded-bl-md bg-stone-100 px-4 py-3 shadow-sm dark:bg-stone-800">
        <div className="flex gap-1.5">
          <span
            className="h-2 w-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <span
            className="h-2 w-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <span
            className="h-2 w-2 rounded-full bg-amber-500 animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
        </div>
      </div>
    </div>
  );
}
