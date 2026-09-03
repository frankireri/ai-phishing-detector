import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [retrainStatus, setRetrainStatus] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (!token || role !== 'admin') {
      navigate('/login');
      return;
    }

    const fetchStats = async () => {
      try {
        const res = await axios.get('/api/analytics', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setStats(res.data);
      } catch (err) {
        console.error('Failed to fetch stats', err);
      }
    };
    fetchStats();
  }, [navigate]);

  const handleRetrain = async () => {
    setLoading(true);
    setRetrainStatus('Retraining model... this may take a moment.');
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post('/api/retrain', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRetrainStatus(res.data.message);
    } catch (err: any) {
      setRetrainStatus(err.response?.data?.error || 'Retraining failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  return (
    <div className="min-h-screen p-8 bg-gray-50 font-sans">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-black uppercase">Admin Dashboard</h1>
        </div>

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 border-2 border-black rounded-sm">
              <h3 className="text-xs font-bold text-gray-500 uppercase">Total Users</h3>
              <p className="text-4xl font-black">{stats.total_users}</p>
            </div>
            <div className="bg-white p-6 border-2 border-black rounded-sm">
              <h3 className="text-xs font-bold text-gray-500 uppercase">Total Scans</h3>
              <p className="text-4xl font-black">{stats.total_scans}</p>
            </div>
            <div className="bg-white p-6 border-2 border-black rounded-sm">
              <h3 className="text-xs font-bold text-gray-500 uppercase">Phishing Detected</h3>
              <p className="text-4xl font-black text-orange-500">{stats.phishing_scans}</p>
            </div>
          </div>
        )}

        <div className="bg-white p-8 border-2 border-black rounded-sm">
          <h2 className="text-xl font-bold uppercase mb-4">Model Management</h2>
          <p className="text-sm text-gray-600 mb-6">Trigger a manual retraining of the Random Forest model using the latest feedback data.</p>
          <button 
            onClick={handleRetrain}
            disabled={loading}
            className="bg-black text-white px-6 py-3 font-bold uppercase text-sm rounded-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Retrain Model'}
          </button>
          {retrainStatus && <p className="mt-4 text-sm font-semibold text-orange-600">{retrainStatus}</p>}
        </div>
      </div>
    </div>
  );
}
