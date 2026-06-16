import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient, Session } from "../api-client";

const SESSION_KEY = "llm-inspector:session_id";

// --- Hooks ---

export const useCreateSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ model_name, prompt }: { model_name: string; prompt: string }) => {
      return apiClient.createSession(model_name, prompt);
    },
    onSuccess: (data) => {
      if (typeof window !== "undefined") {
        localStorage.setItem(SESSION_KEY, data.id);
      }
      queryClient.setQueryData(["session"], data);
    },
  });
};

export const useCurrentSessionId = () => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(SESSION_KEY);
};

export const useTopology = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["topology", sessionId],
    queryFn: () => apiClient.getTopology(sessionId!),
    enabled: !!sessionId,
    refetchInterval: false, // Topology doesn't change
  });
};

export const useMetrics = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["metrics", sessionId],
    queryFn: () => apiClient.getMetrics(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 1000, // Live poll (mocking real-time until WS is fully integrated)
  });
};

export const useAttention = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["attention", sessionId],
    queryFn: () => apiClient.getAttention(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 1000,
  });
};

export const useActivations = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["activations", sessionId],
    queryFn: () => apiClient.getActivations(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 1000,
  });
};

export const useMemory = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["memory", sessionId],
    queryFn: () => apiClient.getMemory(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 1000,
  });
};

export const useTokens = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["tokens", sessionId],
    queryFn: () => apiClient.getTokens(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 1000,
  });
};

export const useAnomalies = (sessionId: string | null) => {
  return useQuery({
    queryKey: ["anomalies", sessionId],
    queryFn: () => apiClient.getAnomalies(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 2000,
  });
};
