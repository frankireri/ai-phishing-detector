"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FiMail, FiMessageSquare, FiShield, FiAlertTriangle, FiCheckCircle, FiLoader, FiClock, FiTag, FiCpu } from "react-icons/fi";
import { api, getErrorMessage } from "@/lib/api";
import { PredictionResult } from "@/types";
import { cn, confidenceColor, formatPercent } from "@/lib/utils";
import toast from "react-hot-toast";

const SAMPLE_PHISHING = "URGENT: Your M-Pesa account has been suspended. Click http://mpesa-verify.duckdns.org/verify?id=8271 to reactivate within 24 hours or your account will be permanently closed.";
const SAMPLE_LEGIT = "Hi, lunch tomorrow at 1pm at the Java House? Let me know if you can make it. See you then!";
const SAMPLE_EMAIL = "Dear Customer, your KCB Bank account has been locked due to suspicious activity. Please verify your identity at http://kcb-secure.co.ke/login to unlock your account immediately.";

export default function Detector() {
  const [text, setText] = useState("");
  const [type, setType] = useState<"email" | "sms">("email");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const taRef = useRef<HTMLTextAreaElement | null>(null);

  const setSample = (kind: "phishing" | "legit" | "email") => {
    if (kind === "phishing") {
      setText(SAMPLE_PHISHING);
      setType("sms");
    } else if (kind === "email") {
      setText(SAMPLE_EMAIL);
      setType("email");
    } else {
      setText(SAMPLE_LEGIT);
      setType("sms");
    }
    setResult(null);
    taRef.current?.focus();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) {
      toast.error("Please enter some message text");
      return;
    }
    if (text.length < 10) {
      toast.error("Message is too short for reliable analysis");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post("/predict", { text, type });
      setResult(res.data.result);
      if (res.data.result.prediction === "phishing") {
        toast.error("⚠️ Phishing detected!");
      } else {
        toast.success("✅ Looks legitimate");
      }
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const isPhishing = result?.prediction === "phishing";
  const confidencePct = result ? result.confidence * 100 : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-100 text-primary-700 text-xs font-semibold mb-4">
          <FiShield className="w-3.5 h-3.5" />
          AI-Powered Detection
        </div>
        <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 mb-3">
          Detect Phishing in <span className="text-primary-600">Seconds</span>
        </h1>
        <p className="text-slate-600 max-w-2xl mx-auto text-lg">
          Paste any email or SMS to instantly classify it as phishing or legitimate
          using machine learning trained on thousands of messages.
        </p>
      </motion.div>

      <div className="grid lg:grid-cols-5 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-3"
        >
          <div className="card">
            <div className="p-6 border-b border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <FiShield className="text-primary-600" />
                  Message Analyzer
                </h2>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setType("email")}
                    className={cn(
                      "px-3 py-1.5 rounded-md text-sm font-medium flex items-center gap-1.5 transition",
                      type === "email"
                        ? "bg-primary-100 text-primary-700"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    )}
                  >
                    <FiMail className="w-4 h-4" />
                    Email
                  </button>
                  <button
                    type="button"
                    onClick={() => setType("sms")}
                    className={cn(
                      "px-3 py-1.5 rounded-md text-sm font-medium flex items-center gap-1.5 transition",
                      type === "sms"
                        ? "bg-primary-100 text-primary-700"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    )}
                  >
                    <FiMessageSquare className="w-4 h-4" />
                    SMS
                  </button>
                </div>
              </div>

              <form onSubmit={handleSubmit}>
                <textarea
                  ref={taRef}
                  className="input min-h-[280px] font-mono text-sm leading-relaxed resize-y"
                  placeholder={
                    type === "email"
                      ? "Paste the email content here (subject + body)..."
                      : "Paste the SMS text here..."
                  }
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  maxLength={50000}
                />
                <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
                  <span>{text.length.toLocaleString()} / 50,000 characters</span>
                  {text.length > 0 && (
                    <button
                      type="button"
                      onClick={() => {
                        setText("");
                        setResult(null);
                      }}
                      className="text-slate-500 hover:text-slate-700"
                    >
                      Clear
                    </button>
                  )}
                </div>

                <div className="mt-4 flex flex-col sm:flex-row gap-3">
                  <button
                    type="submit"
                    disabled={loading || !text.trim()}
                    className="btn-primary flex-1 py-3"
                  >
                    {loading ? (
                      <>
                        <FiLoader className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <FiShield className="w-4 h-4 mr-2" />
                        Analyze Message
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>

            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200">
              <p className="text-xs font-semibold text-slate-600 mb-2">Try a sample:</p>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => setSample("phishing")}
                  className="px-3 py-1.5 text-xs rounded-md bg-red-50 text-red-700 hover:bg-red-100 border border-red-200"
                >
                  Phishing SMS
                </button>
                <button
                  type="button"
                  onClick={() => setSample("email")}
                  className="px-3 py-1.5 text-xs rounded-md bg-orange-50 text-orange-700 hover:bg-orange-100 border border-orange-200"
                >
                  Phishing Email
                </button>
                <button
                  type="button"
                  onClick={() => setSample("legit")}
                  className="px-3 py-1.5 text-xs rounded-md bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200"
                >
                  Legitimate Message
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-2"
        >
          <AnimatePresence mode="wait">
            {result ? (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className={cn(
                  "card overflow-hidden",
                  isPhishing ? "border-red-200" : "border-emerald-200"
                )}
              >
                <div
                  className={cn(
                    "p-6 text-white",
                    isPhishing
                      ? "bg-gradient-to-br from-red-500 to-red-700"
                      : "bg-gradient-to-br from-emerald-500 to-emerald-700"
                  )}
                >
                  <div className="flex items-center gap-3 mb-3">
                    {isPhishing ? (
                      <FiAlertTriangle className="w-10 h-10" />
                    ) : (
                      <FiCheckCircle className="w-10 h-10" />
                    )}
                    <div>
                      <p className="text-xs uppercase tracking-wider opacity-80">Result</p>
                      <h3 className="text-2xl font-bold">
                        {isPhishing ? "Phishing Detected" : "Looks Legitimate"}
                      </h3>
                    </div>
                  </div>
                  <div className="mt-4">
                    <div className="flex items-end justify-between mb-1">
                      <span className="text-sm opacity-90">Confidence</span>
                      <span className="text-2xl font-bold">{confidencePct.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${confidencePct}%` }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                        className="h-full bg-white"
                      />
                    </div>
                  </div>
                </div>

                <div className="p-6 space-y-4">
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-slate-50 rounded-lg p-3">
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        <FiCpu className="w-3.5 h-3.5" />
                        Model
                      </p>
                      <p className="font-semibold capitalize mt-1">
                        {result.model_used.replace(/_/g, " ")}
                      </p>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-3">
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        <FiClock className="w-3.5 h-3.5" />
                        Processing
                      </p>
                      <p className="font-semibold mt-1">{result.processing_time_ms} ms</p>
                    </div>
                  </div>

                  {result.suspicious_keywords && result.suspicious_keywords.length > 0 && (
                    <div>
                      <p className="text-xs font-semibold text-slate-600 mb-2 flex items-center gap-1">
                        <FiTag className="w-3.5 h-3.5" />
                        Suspicious keywords detected
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {result.suspicious_keywords.map((kw) => (
                          <span
                            key={kw}
                            className="badge bg-red-100 text-red-700 border border-red-200"
                          >
                            {kw}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {isPhishing ? (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800">
                      <p className="font-semibold mb-1">⚠️ Recommendations:</p>
                      <ul className="list-disc list-inside space-y-0.5 text-xs">
                        <li>Do not click any links in the message</li>
                        <li>Do not reply with personal information</li>
                        <li>Verify the sender through official channels</li>
                        <li>Report the message to your IT/security team</li>
                      </ul>
                    </div>
                  ) : (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3 text-sm text-emerald-800">
                      <p className="font-semibold mb-1">✓ Safety notes:</p>
                      <p className="text-xs">
                        This message appears legitimate based on our analysis.
                        Always remain vigilant and verify unusual requests through
                        separate, trusted channels.
                      </p>
                    </div>
                  )}
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="card p-8 text-center"
              >
                <div className="w-16 h-16 mx-auto bg-primary-50 rounded-2xl flex items-center justify-center mb-4">
                  <FiShield className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="font-semibold text-slate-900 mb-2">Ready to Analyze</h3>
                <p className="text-sm text-slate-500">
                  Paste a message on the left and click <b>Analyze Message</b> to see the
                  AI classification in action.
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-12">
        {[
          { title: "Real-time", desc: "Sub-100ms classification using TF-IDF + ML" },
          { title: "Multi-algorithm", desc: "LR, Naïve Bayes, Random Forest, SVM compared" },
          { title: "Local context", desc: "Trained on Kenya-focused phishing examples" },
          { title: "Privacy-first", desc: "Messages are not stored when anonymous" },
        ].map((f) => (
          <div key={f.title} className="card p-5">
            <h4 className="font-semibold text-slate-900">{f.title}</h4>
            <p className="text-sm text-slate-600 mt-1">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
