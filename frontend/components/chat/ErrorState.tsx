"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({ message, onRetry, className }: ErrorStateProps) {
  return (
    <div
      className={cn(
        "flex justify-start animate-in fade-in-0 duration-200",
        className
      )}
    >
      <div className="max-w-[85%] rounded-2xl rounded-bl-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-200">
        <p className="font-medium">Something went wrong</p>
        <p className="mt-1 opacity-90">{message}</p>
        {onRetry && (
          <Button
            variant="outline"
            size="sm"
            className="mt-3 border-red-300 text-red-700 hover:bg-red-100 dark:border-red-700 dark:hover:bg-red-900/30"
            onClick={onRetry}
          >
            Try again
          </Button>
        )}
      </div>
    </div>
  );
}
