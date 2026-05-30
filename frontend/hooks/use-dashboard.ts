import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";
import type { FullDashboardData } from "@/types/dashboard";

export function useDashboard() {
  const researchQuery = useQuery({
    queryKey: ["research"],
    queryFn: async () => {
      const response = await api.agent.getResearch({ exam: "KAS" });
      return response.data.data;
    },
  });

  const studentAnalysisQuery = useQuery({
    queryKey: ["studentAnalysis"],
    queryFn: async () => {
      const response = await api.agent.getStudentAnalysis();
      return response.data.data;
    },
  });

  return {
    data: 
      researchQuery.data && studentAnalysisQuery.data
        ? {
            research: researchQuery.data,
            studentAnalysis: studentAnalysisQuery.data,
          }
        : undefined,
    isLoading: researchQuery.isLoading || studentAnalysisQuery.isLoading,
    error: researchQuery.error || studentAnalysisQuery.error,
    refetch: () => {
      researchQuery.refetch();
      studentAnalysisQuery.refetch();
    },
    researchQuery,
    studentAnalysisQuery,
  } as const;
}
