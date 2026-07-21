export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = "ApiError";
  }
}

type ApiOptions = RequestInit & {
  timeoutMs?: number;
  redirectOnUnauthorized?: boolean;
};

export async function apiFetch<T>(path: string, init: ApiOptions = {}): Promise<T> {
  const { timeoutMs = 30000, redirectOnUnauthorized = true, ...requestInit } = init;
  const token = typeof window === "undefined" ? null : localStorage.getItem("token");
  const headers = new Headers(requestInit.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (requestInit.body && !(requestInit.body instanceof FormData)) headers.set("Content-Type", "application/json");

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, { ...requestInit, headers, signal: controller.signal, credentials: "include" });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The server took too long to respond. Please try again.", 408);
    }
    throw new ApiError("Unable to reach the server. Check that the backend and database are running.", 0);
  } finally {
    window.clearTimeout(timeout);
  }

  if (response.status === 204) return undefined as T;
  const data = await response.json().catch(() => null);
  if (response.status === 401 && redirectOnUnauthorized && typeof window !== "undefined") {
    localStorage.removeItem("token");
    window.location.assign("/auth/login");
  }
  if (!response.ok) throw new ApiError(data?.detail || "Request failed", response.status);
  return data as T;
}
