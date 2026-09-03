import { Link, useNavigate } from 'react-router-dom';

export default function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  if (!token) return null;

  return (
    <header className="w-full bg-white border-b-2 border-black px-6 py-4 flex justify-between items-center shadow-sm">
      <div className="flex items-center gap-6">
        <h1 className="text-xl font-black tracking-tighter uppercase text-black">
          PhishDetect<span className="text-orange-500">.</span>
        </h1>
        <nav className="hidden md:flex gap-4 ml-8 text-sm font-bold uppercase tracking-widest">
          <Link to="/dashboard" className="text-gray-500 hover:text-black transition-colors">Scanner</Link>
          <Link to="/history" className="text-gray-500 hover:text-black transition-colors">History</Link>
          {role === 'admin' && (
            <Link to="/admin" className="text-gray-500 hover:text-black transition-colors">Admin</Link>
          )}
        </nav>
      </div>
      <button onClick={handleLogout} className="text-xs font-bold text-gray-500 hover:text-orange-500 uppercase tracking-widest transition-colors">
        Logout
      </button>
    </header>
  );
}
