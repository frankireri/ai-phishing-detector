import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function ScanHistory() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchHistory = async () => {
      try {
        const res = await axios.get('/api/history', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setHistory(res.data);
      } catch (err) {
        console.error('Failed to fetch history', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [navigate]);

  return (
    <div className="min-h-screen p-8 bg-gray-50 font-sans">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-black uppercase mb-8">Scan History</h1>
        
        {loading ? (
          <p className="font-bold text-gray-500 uppercase tracking-widest">Loading history...</p>
        ) : history.length === 0 ? (
          <div className="bg-white p-12 text-center border-2 border-black rounded-sm">
            <p className="text-gray-500 font-bold uppercase tracking-widest">No previous scans found.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {history.map((scan) => (
              <div key={scan.id} className="bg-white p-6 border-2 border-black rounded-sm shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex-grow">
                  <p className="text-sm text-gray-600 mb-2 truncate max-w-2xl">"{scan.message_text}"</p>
                  <p className="text-xs text-gray-400 font-semibold">{new Date(scan.timestamp).toLocaleString()}</p>
                </div>
                <div className="flex items-center gap-6 min-w-max">
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Confidence</p>
                    <p className="text-xl font-black">{scan.confidence}%</p>
                  </div>
                  <div className={`px-4 py-2 border-2 text-xs font-black uppercase tracking-widest rounded-sm ${scan.prediction === 'phishing' ? 'border-orange-500 text-orange-600 bg-orange-50' : 'border-green-500 text-green-600 bg-green-50'}`}>
                    {scan.prediction}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
