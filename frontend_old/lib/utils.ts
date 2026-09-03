import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(iso?: string | null): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export function formatPercent(value: number, digits = 1): string {
  return `${(value * 100).toFixed(digits)}%`;
}

export function confidenceColor(confidence: number, isPhishing: boolean): string {
  if (isPhishing) {
    if (confidence > 0.85) return "text-red-600";
    if (confidence > 0.65) return "text-orange-600";
    return "text-yellow-600";
  }
  if (confidence > 0.85) return "text-emerald-600";
  if (confidence > 0.65) return "text-blue-600";
  return "text-slate-600";
}
