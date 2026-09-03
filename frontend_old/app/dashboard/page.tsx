"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { FiShield, FiAlertTriangle, FiCheckCircle, FiTrendingUp, FiCpu, FiClock, FiBarChart2 } from "react-icons/fi";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend, PieChart, Pie, Cell } from "recharts";
import { api, getErrorMessage } from "@/lib/api";
import { DashboardData, ModelMetric } from "@/types";
import { formatPercent } from "@/lib/utils";
import toast from "react-hot-toast";

const PIE_COLORS = ["#ef4444", "#10b981"];

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [metrics, setMetrics] = useState<ModelMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/analytics/dashboard"), api.get("/training/metrics/latest")])
      .then(([d, m]) => {
        setData(d.data.dashboard);
        setMetrics(m.data.metrics || []);
      })
      .catch((err) => toast.error(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="card p-6 h-32 shimmer" />
          ))}
        </div>
        <div className="card p-6 h-80 shimmer" />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 text-center text-slate-500">
        Failed to load dashboard.
      </div>
    );
  }

  const stats = [
    {
      title: "Total Analyses",
      value: data.total_predictions,
      icon: FiBarChart2,
      color: "text-primary-600 bg-primary-50",
    },
    {
      title: "Phishing Detected",
      value: data.phishing_count,
      icon: FiAlertTriangle,
      color: "text-red-600 bg-red-50",
    },
    {
      title: "Legitimate",
      value: data.legitimate_count,
      icon: FiCheckCircle,
      color: "text-emerald-600 bg-emerald-50",
    },
    {
      title: "Phishing Rate",
      value: `${data.phishing_rate}%`,
      icon: FiTrendingUp,
      color: "text-orange-600 bg-orange-50",
    },
  ];

  const pieData = [
    { name: "Phishing", value: data.phishing_count },
    { name: "Legitimate", value: data.legitimate_count },
  ];

  const typeData = Object.entries(data.type_breakdown).map(([k, v]) => ({
    type: k,
    Phishing: v.phishing,
    Legitimate: v.legitimate,
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-600 mt-1">Overview of your phishing detection activity.</p>
      </motion.div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s, i) => {
          const Icon = s.icon;
          return (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="card p-6"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-slate-500">{s.title}</p>
                  <p className="text-3xl font-bold text-slate-900 mt-1">{s.value}</p>
                </div>
                <div className={`p-2.5 rounded-lg ${s.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Prediction Distribution</h3>
          {data.total_predictions > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={90}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart
              text="No predictions yet. Try the detector to see your stats here!"
              cta
            />
          )}
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Email vs SMS Breakdown</h3>
          {typeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={typeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="type" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="Phishing" fill="#ef4444" radius={[6, 6, 0, 0]} />
                <Bar dataKey="Legitimate" fill="#10b981" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart text="No data yet" />
          )}
        </div>
      </div>

      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
            <FiCpu className="text-primary-600" />
            Model Performance
          </h3>
          <Link href="/analytics" className="text-sm text-primary-600 hover:text-primary-700">
            View all →
          </Link>
        </div>
        {metrics.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500 border-b border-slate-200">
                  <th className="py-2 font-medium">Algorithm</th>
                  <th className="py-2 font-medium">Accuracy</th>
                  <th className="py-2 font-medium">Precision</th>
                  <th className="py-2 font-medium">Recall</th>
                  <th className="py-2 font-medium">F1-Score</th>
                  <th className="py-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {metrics.map((m) => (
                  <tr key={m.id} className="border-b border-slate-100">
                    <td className="py-3 font-medium capitalize">{m.algorithm.replace(/_/g, " ")}</td>
                    <td className="py-3">{formatPercent(m.accuracy, 2)}</td>
                    <td className="py-3">{formatPercent(m.precision, 2)}</td>
                    <td className="py-3">{formatPercent(m.recall, 2)}</td>
                    <td className="py-3 font-semibold">{formatPercent(m.f1_score, 2)}</td>
                    <td className="py-3">
                      {m.is_active ? (
                        <span className="badge bg-emerald-100 text-emerald-700">Active</span>
                      ) : (
                        <span className="badge bg-slate-100 text-slate-600">Inactive</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyChart text="No trained models yet. Run the training pipeline from the backend." />
        )}
      </div>
    </div>
  );
}

function EmptyChart({ text, cta }: { text: string; cta?: boolean }) {
  return (
    <div className="h-[280px] flex flex-col items-center justify-center text-slate-400 text-sm">
      <FiBarChart2 className="w-10 h-10 mb-2" />
      <p>{text}</p>
      {cta && (
        <Link href="/" className="btn-primary mt-3 text-xs">
          Try the Detector
        </Link>
      )}
    </div>
  );
}
