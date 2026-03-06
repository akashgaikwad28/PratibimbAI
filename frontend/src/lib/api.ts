import { supabase } from "./supabase";

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token ? { "Authorization": `Bearer ${token}` } : {}),
            ...options.headers,
        },
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(error.detail || "API request failed");
    }

    return response.json();
}

export const api = {
    generate: (data: any) => fetchWithAuth("/generate", {
        method: "POST",
        body: JSON.stringify(data),
    }),
    getJob: (jobId: string) => fetchWithAuth(`/job/${jobId}`),
    getProfile: () => fetchWithAuth("/profile"),
    updateProfile: (data: any) => fetchWithAuth("/profile", {
        method: "PATCH",
        body: JSON.stringify(data),
    }),
    // Sources
    getSources: () => fetchWithAuth("/api/sources"),
    addSource: (data: any) => fetchWithAuth("/api/sources", {
        method: "POST",
        body: JSON.stringify(data),
    }),
    updateSource: (id: string, data: any) => fetchWithAuth(`/api/sources/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
    }),
    deleteSource: (id: string) => fetchWithAuth(`/api/sources/${id}`, {
        method: "DELETE",
    }),
};
