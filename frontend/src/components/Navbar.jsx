import { Link, useNavigate } from "react-router-dom";
import { logout } from "../utils/auth";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white p-4 shadow-lg border-b border-slate-700">
      <div className="max-w-[1400px] mx-auto px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-1 text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            🌳 TokenTree
          </div>
          <div className="flex gap-6">
            <Link
              to="/dashboard"
              className="text-slate-300 hover:text-blue-400 font-medium transition-colors duration-200 relative group"
            >
              Dashboard
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-400 group-hover:w-full transition-all duration-300"></span>
            </Link>
            <Link
              to="/add-crypto"
              className="text-slate-300 hover:text-blue-400 font-medium transition-colors duration-200 relative group"
            >
              Add Crypto
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-400 group-hover:w-full transition-all duration-300"></span>
            </Link>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-6 py-2 rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-red-500/50"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
