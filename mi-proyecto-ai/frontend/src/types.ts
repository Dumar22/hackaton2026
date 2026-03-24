export type ModelName = 'gpt' | 'gemini' | 'kimi';

export interface PipelineMetadata {
  version?: string;
  total_records?: number;
  accuracy?: number;
  average_confidence?: number;
  model?: string;
  random_seed?: number;
  execution_date?: string;
  version_es?: string;
  total_registros?: number;
  confianza_promedio?: number;
  modelo?: string;
  fecha_ejecucion?: string;
  [key: string]: unknown;
}

export interface MetadataResponse {
  metadata?: PipelineMetadata;
  acciones_automaticas?: Record<string, number>;
  distribucion_predicciones?: Record<string, number>;
  [key: string]: unknown;
}

export interface Prediction {
  id: string;
  tipo_proceso: string;
  canal: string;
  prediccion_clase: string;
  confianza_prediccion: number;
  accion_automatica: string;
  prioridad_automatica: string;
  asignado_a: string;
}

export interface ProcessAIResponse {
  success: boolean;
  result?: unknown;
  history_id?: string;
}

export interface ProcessHistoryItem {
  id: string;
  timestamp: string;
  file_name: string;
  model: ModelName;
  success: boolean;
  error: string | null;
  result_preview: string | null;
}
