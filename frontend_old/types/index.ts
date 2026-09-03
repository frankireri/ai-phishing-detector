export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_admin: boolean;
  created_at?: string;
  last_login?: string;
}

export interface PredictionResult {
  prediction: "phishing" | "legitimate";
  confidence: number;
  model_used: string;
  suspicious_keywords: string[];
  processing_time_ms: number;
  message_type?: string;
  input_length?: number;
  id?: number;
}

export interface PredictResponse {
  success: boolean;
  result: PredictionResult;
}

export interface ModelMetric {
  id: number;
  algorithm: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  training_samples: number;
  test_samples: number;
  training_time_seconds?: number;
  confusion_matrix?: number[][];
  is_active: boolean;
  created_at: string;
}

export interface HistoryItem extends PredictionResult {
  id: number;
  user_id?: number;
  message_type: string;
  created_at: string;
}

export interface DashboardSummary {
  total_predictions: number;
  phishing_detected: number;
  legitimate_detected: number;
  phishing_rate: number;
  average_confidence: number;
  daily_breakdown: Record<string, { phishing: number; legitimate: number }>;
}

export interface DashboardData {
  total_predictions: number;
  phishing_count: number;
  legitimate_count: number;
  phishing_rate: number;
  type_breakdown: Record<string, { phishing: number; legitimate: number }>;
  active_models: ModelMetric[];
}
