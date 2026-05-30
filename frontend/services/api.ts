
import axios from "axios";
import { env } from "@/utils/env";
import type { 
  UserProfile, AgentStatus, DashboardData, 
  ResearchResponse, StudentAnalysisResponse,
  PlanningResponse, PlanningRequest,
  TaskListResponse, TaskResponse, TaskCreate, TaskUpdate,
  RevisionRequest, RevisionResponse,
  ReplanningRequest, ReplanningResponse,
  InsightsResponse, AgentsStatusResponse
} from "@/types/dashboard";

export const apiClient = axios.create({
  baseURL: env.NEXT_PUBLIC_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  },
);

export const api = {
  dashboard: {
    get: () => apiClient.get<DashboardData>("/dashboard"),
  },
  tasks: {
    get: () => apiClient.get<TaskListResponse>("/tasks"),
    create: (data: TaskCreate) => apiClient.post<TaskResponse>("/tasks", data),
    update: (taskId: string, data: TaskUpdate) => apiClient.patch<TaskResponse>(`/tasks/${taskId}`, data),
    delete: (taskId: string) => apiClient.delete(`/tasks/${taskId}`),
  },
  agent: {
    getResearch: (data?: { exam?: string }) =>
      apiClient.post<ResearchResponse>("/agent/research", data || {}),
    getStudentAnalysis: (data?: { refresh?: boolean; student_data?: any }) =>
      apiClient.post<StudentAnalysisResponse>("/agent/student-analysis", data || {}),
    getPlanner: (data?: PlanningRequest) =>
      apiClient.post<PlanningResponse>("/agent/planner", data || {}),
    getRevision: (data?: RevisionRequest) =>
      apiClient.post<RevisionResponse>("/agent/revision", data || {}),
    getReplan: (data?: ReplanningRequest) =>
      apiClient.post<ReplanningResponse>("/agent/replan", data || {}),
    getInsights: () => apiClient.get<InsightsResponse>("/agent/insights"),
    getStatus: () => apiClient.get<AgentsStatusResponse>("/agent/status"),
  },
  user: {
    updateProfile: (data: UserProfile) =>
      apiClient.post("/user/profile", data),
  },
};
