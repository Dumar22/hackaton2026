import axios, { AxiosError } from 'axios';
import type { MetadataResponse, ModelName, Prediction, ProcessAIResponse, ProcessHistoryItem } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function parseApiError(err: unknown, fallback: string): string {
  if (err instanceof AxiosError) {
    if (err.code === 'ERR_NETWORK') {
      return 'Network Error: verifica que backend (8000) y CORS esten activos.';
    }
    const detail = err.response?.data as { detail?: string } | undefined;
    return detail?.detail ?? err.message;
  }
  if (err instanceof Error) {
    return err.message;
  }
  return fallback;
}

function csvToPredictions(csvText: string): Prediction[] {
  const lines = csvText.trim().split('\n').filter(Boolean);
  if (lines.length <= 1) {
    return [];
  }

  const headers = lines[0].split(',').map((header) => header.trim());

  return lines.slice(1).map((line) => {
    const values = line.split(',');
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] ?? '']));

    return {
      id: row.id ?? '',
      tipo_proceso: row.tipo_proceso ?? '',
      canal: row.canal ?? '',
      prediccion_clase: row.prediccion_clase ?? '',
      confianza_prediccion: Number(row.confianza_prediccion ?? 0),
      accion_automatica: row.accion_automatica ?? '',
      prioridad_automatica: row.prioridad_automatica ?? '',
      asignado_a: row.asignado_a ?? '',
    };
  });
}

export async function processAI(file: File, model: ModelName = 'gpt'): Promise<ProcessAIResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('model', model);

  try {
    const response = await api.post<ProcessAIResponse>('/process-ai', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (err) {
    throw new Error(parseApiError(err, 'Error al procesar el archivo'));
  }
}

export async function getAvailableModels(): Promise<unknown> {
  const response = await api.get('/models');
  return response.data;
}

export async function getMetadata(): Promise<MetadataResponse> {
  try {
    const response = await api.get<MetadataResponse>('/results/metadata');
    return response.data;
  } catch (err) {
    throw new Error(parseApiError(err, 'No se pudieron obtener metadatos'));
  }
}

export async function getPredictions(): Promise<Prediction[]> {
  try {
    const response = await api.get<string>('/results/predictions', { responseType: 'text' });
    return csvToPredictions(response.data);
  } catch (err) {
    throw new Error(parseApiError(err, 'No se pudieron obtener predicciones'));
  }
}

export async function analyzeFile(file: File): Promise<unknown> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/data/analyze-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (err) {
    throw new Error(parseApiError(err, 'No se pudo analizar el archivo'));
  }
}

export async function getProcessHistory(limit: number = 50): Promise<ProcessHistoryItem[]> {
  try {
    const response = await api.get<{ total: number; items: ProcessHistoryItem[] }>(`/process-history?limit=${limit}`);
    return response.data.items;
  } catch (err) {
    throw new Error(parseApiError(err, 'No se pudo obtener historial de procesos'));
  }
}

export const apiService = {
  getMetadata,
  getPredictions,
  analyzeFile,
  getProcessHistory,
};

export default api;
