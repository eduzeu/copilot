export function getToken(): string | null {
  return typeof window === "undefined" ? null : localStorage.getItem("token");
}

export function clearToken(): void {
  localStorage.removeItem("token");
}
