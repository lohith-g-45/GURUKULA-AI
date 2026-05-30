import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/services/health.service";

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 30000,
  });
}
