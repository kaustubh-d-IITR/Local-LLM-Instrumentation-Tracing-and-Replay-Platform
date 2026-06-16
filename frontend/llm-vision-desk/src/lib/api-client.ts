// API Client mapping to Backend FastAPI Schema

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// --- Types mapping to Backend exactly ---
export interface TopologyBlock {
  id?: number;
  session_id: string;
  blocks: any[]; // JSONB in backend
}

export interface Metric {
  id: string;
  session_id: string;
  t: number;
  layer: number;
  op: string;
  dur_ms: number;
  shape: string;
  dtype: string;
  device: string;
  level: "info" | "warn" | "error";
}

export interface Attention {
  id: number;
  session_id: string;
  layer: number;
  head: number;
  matrix: number[][];
}

export interface Activation {
  id: number;
  session_id: string;
  layer: number;
  mean: number;
  max: number;
  min: number;
  variance: number;
  sparsity: number;
}

export interface Anomaly {
  id: string;
  session_id: string;
  t: number;
  severity: "info" | "warn" | "error";
  layer: number;
  message: string;
}

export interface Memory {
  id: number;
  session_id: string;
  t: number;
  gpu: number;
  cpu: number;
}

export interface Token {
  id: number;
  session_id: string;
  idx: int;
  token: string;
  ms: number;
}

export interface Session {
  id: string;
  model_name: string;
  prompt: string;
  status: string;
  created_at: string;
}

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async createSession(model_name: string, prompt: string): Promise<Session> {
    return this.request<Session>("/sessions/start", {
      method: "POST",
      body: JSON.stringify({ model_name, prompt }),
    });
  }

  async getTopology(sessionId: string): Promise<TopologyBlock> {
    return this.request<TopologyBlock>(`/sessions/${sessionId}/topology`);
  }

  async getMetrics(sessionId: string): Promise<Metric[]> {
    return this.request<Metric[]>(`/sessions/${sessionId}/metrics`);
  }

  async getAttention(sessionId: string): Promise<Attention[]> {
    return this.request<Attention[]>(`/sessions/${sessionId}/attention`);
  }

  async getActivations(sessionId: string): Promise<Activation[]> {
    return this.request<Activation[]>(`/sessions/${sessionId}/activations`);
  }

  async getAnomalies(sessionId: string): Promise<Anomaly[]> {
    return this.request<Anomaly[]>(`/sessions/${sessionId}/anomalies`);
  }

  async getMemory(sessionId: string): Promise<Memory[]> {
    return this.request<Memory[]>(`/sessions/${sessionId}/memory`);
  }

  async getTokens(sessionId: string): Promise<Token[]> {
    return this.request<Token[]>(`/sessions/${sessionId}/tokens`);
  }
}

export const apiClient = new ApiClient();
