import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Auth({ isLogin }: { isLogin: boolean }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isLogin ? '/api/login' : '/api/register';
      const response = await axios.post(endpoint, { username, password });
      
      if (isLogin) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('role', response.data.role);
        if (response.data.role === 'admin') {
          navigate('/admin');
        } else {
          navigate('/dashboard');
        }
      } else {
        navigate('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gray-50 font-sans">
      <div className="bg-white p-8 rounded-sm shadow-md border-2 border-black w-full max-w-md">
        <h2 className="text-3xl font-black text-black mb-6 text-center uppercase tracking-tight">
          {isLogin ? 'Login' : 'Register'}
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-semibold text-black mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-gray-50 border border-gray-200 p-3 text-black focus:outline-none focus:border-orange-500 rounded-sm"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-black mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-gray-50 border border-gray-200 p-3 text-black focus:outline-none focus:border-orange-500 rounded-sm"
              required
            />
          </div>
          {error && <p className="text-red-500 text-sm font-semibold">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white font-bold uppercase tracking-widest py-4 mt-2 hover:bg-orange-600 transition-colors rounded-sm shadow-md"
          >
            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>
        <div className="mt-6 text-center text-sm">
          {isLogin ? (
            <p>Don't have an account? <a href="/register" className="text-orange-500 font-bold">Register</a></p>
          ) : (
            <p>Already have an account? <a href="/login" className="text-orange-500 font-bold">Login</a></p>
          )}
        </div>
      </div>
    </div>
  );
}
