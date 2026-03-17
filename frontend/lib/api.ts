import { z } from "zod";
import type { components } from "./api-types.generated";

const CookingResponseSchema = z.object({
  refusal: z.string().nullable(),
  answer: z.string().nullable(),
  reasoning_chain: z.array(z.record(z.unknown())).nullable().optional(),
});

/** Response type; kept in sync with OpenAPI (see lib/api-types.generated.ts). */
export type CookingResponse = components["schemas"]["CookingResponse"];

/** Backend API base URL. Use port 8000 for local/Docker. */
function getBaseUrl(): string {
  if (typeof window === "undefined") return "";
  const env = (process.env.NEXT_PUBLIC_API_URL ?? "").trim();
  return env ? env.replace(/\/+$/, "") : "http://localhost:8000";
}

export async function sendCookingMessage(
  message: string,
  debug = false
): Promise<CookingResponse> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/cooking`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, debug }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  const data = await res.json();
  return CookingResponseSchema.parse(data);
}

export async function streamCookingMessage(
  message: string,
  onChunk: (data: CookingResponse) => void,
  debug = false
): Promise<void> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/cooking/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, debug }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response body");
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const json = JSON.parse(line.slice(6)) as unknown;
          const parsed = CookingResponseSchema.parse(json);
          onChunk(parsed);
        } catch {
          // skip invalid or partial lines
        }
      }
    }
  }
}
