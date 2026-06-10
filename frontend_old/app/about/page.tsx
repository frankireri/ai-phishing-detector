import { FiShield, FiCpu, FiMail, FiLock, FiBarChart2, FiCode, FiTarget, FiBookOpen, FiAward } from "react-icons/fi";

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 text-primary-600 rounded-2xl mb-4">
          <FiShield className="w-8 h-8" />
        </div>
        <h1 className="text-4xl font-bold text-slate-900">About PhishGuard AI</h1>
        <p className="text-slate-600 mt-3 max-w-2xl mx-auto">
          A final year research project exploring the application of Artificial
          Intelligence to phishing detection in email and SMS communication.
        </p>
      </div>

      <div className="card p-8 mb-8">
        <h2 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <FiBookOpen className="text-primary-600" />
          Project Overview
        </h2>
        <p className="text-slate-600 leading-relaxed mb-4">
          This project designs and implements a comprehensive AI-based phishing
          detection system for email and SMS communications. Phishing remains one
          of the most prevalent cybersecurity threats globally and particularly
          in Kenya, where attackers frequently impersonate banks, mobile money
          services, government institutions, and e-commerce platforms.
        </p>
        <p className="text-slate-600 leading-relaxed">
          Traditional rule-based detection mechanisms rely heavily on blacklists
          and static keyword filters, which are ineffective against rapidly
          evolving phishing strategies. This project proposes a machine
          learning-driven approach capable of learning patterns from historical
          datasets and accurately classifying messages as either phishing or
          legitimate.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div className="card p-6">
          <h3 className="text-xl font-bold text-slate-900 mb-3 flex items-center gap-2">
            <FiTarget className="text-red-500" />
            General Objective
          </h3>
          <p className="text-slate-600">
            To design and implement a web-based AI-powered phishing detection
            system for email and SMS communication.
          </p>
        </div>
        <div className="card p-6">
          <h3 className="text-xl font-bold text-slate-900 mb-3 flex items-center gap-2">
            <FiAward className="text-emerald-500" />
            Specific Objectives
          </h3>
          <ul className="text-slate-600 space-y-1.5 text-sm">
            <li>• Collect and preprocess phishing & legitimate datasets</li>
            <li>• Train and compare ML classification models</li>
            <li>• Evaluate models using accuracy, precision, recall, F1</li>
            <li>• Implement a secure web-based prototype</li>
            <li>• Compare with traditional rule-based methods</li>
          </ul>
        </div>
      </div>

      <div className="card p-8 mb-8">
        <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
          <FiCpu className="text-primary-600" />
          Technology Stack
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { icon: FiCode, title: "Backend", items: ["Flask", "Python 3.x", "Gunicorn"] },
            { icon: FiCpu, title: "Machine Learning", items: ["Scikit-learn", "NLTK", "TF-IDF", "Joblib"] },
            { icon: FiMail, title: "Frontend", items: ["Next.js 14", "TypeScript", "Tailwind CSS", "Framer Motion"] },
            { icon: FiBarChart2, title: "Visualization", items: ["Recharts", "React Hot Toast"] },
            { icon: FiLock, title: "Security", items: ["JWT Auth", "bcrypt", "Flask-Limiter"] },
            { icon: FiShield, title: "Database", items: ["SQLAlchemy", "PostgreSQL / SQLite"] },
          ].map((s) => {
            const Icon = s.icon;
            return (
              <div key={s.title} className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <Icon className="w-5 h-5 text-primary-600 mb-2" />
                <h4 className="font-semibold text-slate-900 mb-1.5">{s.title}</h4>
                <p className="text-xs text-slate-600">{s.items.join(" • ")}</p>
              </div>
            );
          })}
        </div>
      </div>

      <div className="card p-8 mb-8">
        <h2 className="text-2xl font-bold text-slate-900 mb-6">ML Algorithms Compared</h2>
        <div className="grid sm:grid-cols-2 gap-4">
          {[
            {
              name: "Logistic Regression",
              desc: "Probabilistic linear classifier; efficient for high-dimensional sparse text features.",
            },
            {
              name: "Naïve Bayes (Multinomial)",
              desc: "Probabilistic model based on Bayes' theorem; classical baseline for spam detection.",
            },
            {
              name: "Random Forest",
              desc: "Ensemble of decision trees; reduces overfitting and handles non-linear patterns.",
            },
            {
              name: "Support Vector Machine (Linear)",
              desc: "Margin-based classifier; strong performance on text classification tasks.",
            },
          ].map((a) => (
            <div key={a.name} className="p-4 rounded-lg border border-slate-200">
              <h4 className="font-semibold text-slate-900 mb-1">{a.name}</h4>
              <p className="text-sm text-slate-600">{a.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="card p-8">
        <h2 className="text-2xl font-bold text-slate-900 mb-6">Project Team</h2>
        <div className="grid sm:grid-cols-2 gap-6">
          <div className="p-5 rounded-lg bg-gradient-to-br from-primary-50 to-primary-100 border border-primary-200">
            <p className="text-xs uppercase tracking-wider text-primary-700 font-semibold">Student</p>
            <h3 className="text-lg font-bold text-slate-900 mt-1">Maximillian Saitabau</h3>
            <p className="text-sm text-slate-600">Admission: 1061592</p>
            <p className="text-sm text-slate-600">BSc. Computer Science</p>
          </div>
          <div className="p-5 rounded-lg bg-gradient-to-br from-emerald-50 to-emerald-100 border border-emerald-200">
            <p className="text-xs uppercase tracking-wider text-emerald-700 font-semibold">Supervisor</p>
            <h3 className="text-lg font-bold text-slate-900 mt-1">Prof. Joel Barasa</h3>
            <p className="text-sm text-slate-600">Department of Computer Science</p>
            <p className="text-sm text-slate-600">Faculty of Science</p>
          </div>
        </div>
        <div className="mt-6 text-center text-sm text-slate-500">
          Catholic University of Eastern Africa (CUEA) — Final Year Project
        </div>
      </div>
    </div>
  );
}
