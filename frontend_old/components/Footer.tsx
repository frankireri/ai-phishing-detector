import { FiShield, FiGithub, FiMail } from "react-icons/fi";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <div className="bg-primary-600 text-white p-2 rounded-lg">
                <FiShield className="w-5 h-5" />
              </div>
              <div>
                <p className="font-bold text-white">PhishGuard AI</p>
                <p className="text-xs text-slate-400">CUEA Final Year Project</p>
              </div>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              An AI-based phishing detection system for email and SMS communication.
              Powered by machine learning and natural language processing.
            </p>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/" className="hover:text-white">Detector</Link></li>
              <li><Link href="/dashboard" className="hover:text-white">Dashboard</Link></li>
              <li><Link href="/analytics" className="hover:text-white">Analytics</Link></li>
              <li><Link href="/about" className="hover:text-white">About</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">Project Info</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>Student: Maximillian Saitabau (1061592)</li>
              <li>Supervisor: Prof. Joel Barasa</li>
              <li>Institution: Catholic University of Eastern Africa</li>
              <li>Department: Computer Science</li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-sm text-slate-400">
          <p>© {new Date().getFullYear()} PhishGuard AI. Academic use only.</p>
          <p>Built with Next.js, Flask, and scikit-learn</p>
        </div>
      </div>
    </footer>
  );
}
