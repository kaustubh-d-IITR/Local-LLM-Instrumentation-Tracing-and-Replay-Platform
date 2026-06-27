import { i as useQueryClient, n as useQuery, t as useMutation } from "../_libs/tanstack__react-query.mjs";
import { n as clsx } from "../_libs/class-variance-authority+clsx.mjs";
import { t as twMerge } from "../_libs/tailwind-merge.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/utils-C2sR9Z8l.js
var API_URL = "http://localhost:8000";
var ApiClient = class {
	async request(endpoint, options = {}) {
		const response = await fetch(`${API_URL}${endpoint}`, {
			...options,
			headers: {
				"Content-Type": "application/json",
				...options.headers
			}
		});
		if (!response.ok) throw new Error(`API Error: ${response.status} ${response.statusText}`);
		return response.json();
	}
	async createSession(model_name, prompt) {
		return this.request("/sessions/start", {
			method: "POST",
			body: JSON.stringify({
				model_name,
				prompt
			})
		});
	}
	async getTopology(sessionId) {
		return this.request(`/sessions/${sessionId}/topology`);
	}
	async getMetrics(sessionId) {
		return this.request(`/sessions/${sessionId}/metrics`);
	}
	async getAttention(sessionId) {
		return this.request(`/sessions/${sessionId}/attention`);
	}
	async getActivations(sessionId) {
		return this.request(`/sessions/${sessionId}/activations`);
	}
	async getAnomalies(sessionId) {
		return this.request(`/sessions/${sessionId}/anomalies`);
	}
	async getMemory(sessionId) {
		return this.request(`/sessions/${sessionId}/memory`);
	}
	async getTokens(sessionId) {
		return this.request(`/sessions/${sessionId}/tokens`);
	}
};
var apiClient = new ApiClient();
var SESSION_KEY = "llm-inspector:session_id";
var useCreateSession = () => {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async ({ model_name, prompt }) => {
			return apiClient.createSession(model_name, prompt);
		},
		onSuccess: (data) => {
			if (typeof window !== "undefined") localStorage.setItem(SESSION_KEY, data.id);
			queryClient.setQueryData(["session"], data);
		}
	});
};
var useCurrentSessionId = () => {
	if (typeof window === "undefined") return null;
	return localStorage.getItem(SESSION_KEY);
};
var useTopology = (sessionId) => {
	return useQuery({
		queryKey: ["topology", sessionId],
		queryFn: () => apiClient.getTopology(sessionId),
		enabled: !!sessionId,
		refetchInterval: false
	});
};
var useMetrics = (sessionId) => {
	return useQuery({
		queryKey: ["metrics", sessionId],
		queryFn: () => apiClient.getMetrics(sessionId),
		enabled: !!sessionId,
		refetchInterval: 1e3
	});
};
var useAttention = (sessionId) => {
	return useQuery({
		queryKey: ["attention", sessionId],
		queryFn: () => apiClient.getAttention(sessionId),
		enabled: !!sessionId,
		refetchInterval: 1e3
	});
};
var useActivations = (sessionId) => {
	return useQuery({
		queryKey: ["activations", sessionId],
		queryFn: () => apiClient.getActivations(sessionId),
		enabled: !!sessionId,
		refetchInterval: 1e3
	});
};
var useMemory = (sessionId) => {
	return useQuery({
		queryKey: ["memory", sessionId],
		queryFn: () => apiClient.getMemory(sessionId),
		enabled: !!sessionId,
		refetchInterval: 1e3
	});
};
var useTokens = (sessionId) => {
	return useQuery({
		queryKey: ["tokens", sessionId],
		queryFn: () => apiClient.getTokens(sessionId),
		enabled: !!sessionId,
		refetchInterval: 1e3
	});
};
var useAnomalies = (sessionId) => {
	return useQuery({
		queryKey: ["anomalies", sessionId],
		queryFn: () => apiClient.getAnomalies(sessionId),
		enabled: !!sessionId,
		refetchInterval: 2e3
	});
};
function cn(...inputs) {
	return twMerge(clsx(inputs));
}
//#endregion
export { useCreateSession as a, useMetrics as c, useAttention as i, useTokens as l, useActivations as n, useCurrentSessionId as o, useAnomalies as r, useMemory as s, cn as t, useTopology as u };
