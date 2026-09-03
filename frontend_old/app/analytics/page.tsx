"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FiBarChart2, FiClock, FiCpu, FiCheckCircle } from "react-icons/fi";
import { api, getErrorMessage } from "@/lib/api";
import { ModelMetric, HistoryItem } from "@/types";
import { formatDate, formatPercent } from "@/lib/utils";
import toast from "react-hot-toast";

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<ModelMetric[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);

  useEffect(() => {
    api
      .get("/training/metrics")
      .then((r) => setMetrics(r.data.metrics))
      .catch((err) => toast.error(getErrorMessage(err)));
  }, []);

  useEffect(() => {
    api
      .get(`/analytics/history?page=${page}&per_page=20`)
      .then((r) => {
        setHistory(r.data.items);
        setPages(r.data.pages);
      })
      .catch((err) => toast.error(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Analytics</h1>
        <p className="text-slate-600 mt-1">Detailed model metrics and prediction history.</p>
      </motion.div>

      <div className="card p-6 mb-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
          <FiCpu className="text-primary-600" />
          Model Comparison
        </h2>
        {metrics.length > 0 ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {metrics.map((m, i) => (
              <motion.div
                key={m.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`p-5 rounded-xl border ${
                  m.is_active ? "border-emerald-300 bg-emerald-50" : "border-slate-200 bg-white"
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold capitalize text-slate-900">
                    {m.algorithm.replace(/_/g, " ")}
                  </h3>
                  {m.is_active && (
                    <span className="badge bg-emerald-600 text-white">
                      <FiCheckCircle className="w-3 h-3 mr-1" /> Active
                    </span>
                  )}
                </div>
                <div className="space-y-1.5 text-sm">
                  <Row label="Accuracy" value={formatPercent(m.accuracy, 2)} />
                  <Row label="Precision" value={formatPercent(m.precision, 2)} />
                  <Row label="Recall" value={formatPercent(m.recall, 2)} />
                  <Row label="F1-Score" value={formatPercent(m.f1_score, 2)} bold />
                  {m.training_time_seconds != null && (
                    <Row label="Train time" value={`${m.training_time_seconds.toFixed(2)}s`} />
                  )}
                </div>
                {m.confusion_matrix && (
                  <div className="mt-3 text-xs text-slate-500">
                    <p className="font-medium mb-1">Confusion matrix:</p>
                    <pre className="bg-slate-100 p-2 rounded text-[10px]">
                      {JSON.stringify(m.confusion_matrix)}
                    </pre>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-sm">No model metrics available. Train the models first.</p>
        )}
      </div>

      <div className="card p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
          <FiClock className="text-primary-600" />
          Prediction History
        </h2>
        {loading ? (
          <div className="space-y-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-14 shimmer rounded-lg" />
            ))}
          </div>
        ) : history.length > 0 ? (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-500 border-b border-slate-200">
                    <th className="py-2 font-medium">When</th>
                    <th className="py-2 font-medium">Type</th>
                    <th className="py-2 font-medium">Result</th>
                    <th className="py-2 font-medium">Confidence</th>
                    <th className="py-2 font-medium">Model</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h) => (
                    <tr key={h.id} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="py-2.5 text-slate-600">{formatDate(h.created_at)}</td>
                      <td className="py-2.5 capitalize">{h.message_type}</td>
                      <td className="py-2.5">
                        <span
                          className={`badge ${
                            h.prediction === "phishing"
                              ? "bg-red-100 text-red-700"
                              : "bg-emerald-100 text-emerald-700"
                          }`}
                        >
                          {h.prediction}
                        </span>
                      </td>
                      <td className="py-2.5 font-medium">{formatPercent(h.confidence, 1)}</td>
                      <td className="py-2.5 capitalize text-slate-600">
                        {h.model_used.replace(/_/g, " ")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {pages > 1 && (
              <div className="flex items-center justify-between mt-4 text-sm">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="btn-secondary"
                >
                  Previous
                </button>
                <span className="text-slate-500">
                  Page {page} of {pages}
                </span>
                <button
                  onClick={() => setPage((p) => Math.min(pages, p + 1))}
                  disabled={page === pages}
                  className="btn-secondary"
                >
                  Next
                </button>
              </div>
            )}
          </>
        ) : (
          <p className="text-slate-500 text-sm py-8 text-center">
            No prediction history yet. Authenticated predictions are logged here.
          </p>
        )}
      </div>
    </div>
  );
}

function Row({ label, value, bold }: { label: string; value: string; bold?: boolean }) {
  return (
    <div className="flex justify-between">
      <span className="text-slate-500">{label}</span>
      <span className={bold ? "font-bold text-slate-900" : "text-slate-700"}>{value}</span>
    </div>
  );
}
