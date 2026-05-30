import { apiClient } from "@/services/api";

export interface HealthResponse {
  status: string;
  project: string;
  backend: string;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await apiClient.get("/health");
  return response.data;
}
