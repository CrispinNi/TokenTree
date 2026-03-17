import React from "react";
import {
  PieChart,
  Layers,
  Zap,
  Wallet,
  LineChart,
  ShieldCheck,
  Globe,
} from "lucide-react";

const LandingPage = () => {
  // REPLACE THIS URL with the link to the mobile dashboard image I generated for you
  const mobileDashboardImg =
    "https://googleusercontent.com/image_generation_content/3";

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#050816] via-[#0a0f2c] to-[#050816] text-white font-sans selection:bg-cyan-500/30 overflow-x-hidden">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto relative z-20">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
            <Layers size={24} className="text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">
            TOKEN<span className="text-cyan-400">TREE</span>
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
          <a href="#" className="hover:text-white transition-colors">
            Dashboard
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Add Crypto
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Security
          </a>
        </div>

        <button className="bg-red-500 px-6 py-2 rounded-lg text-sm font-semibold hover:bg-red-600 transition-all">
          Logout
        </button>
      </nav>

      {/* Hero Section */}
      <header className="px-6 pt-16 pb-12 text-center max-w-4xl mx-auto relative z-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 text-xs text-cyan-300 mb-6">
          <Zap size={14} />
          <span>Real-time Portfolio Syncing Active</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-gradient-to-b from-white to-gray-500 bg-clip-text text-transparent">
          TRACK AND MANAGE <br /> YOUR PORTFOLIO
        </h1>
        <p className="text-gray-400 text-lg md:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
          The ultimate interface for TokenTree users. View your $81,692.07 and
          growing assets across every chain.
        </p>
      </header>

      {/* Feature Section with Phone Mockup */}
      <section className="px-6 py-20 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
        {/* Left Side: Copy */}
        <div className="space-y-8">
          <div className="p-10 rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur-xl border-l-cyan-500 border-l-4">
            <h2 className="text-4xl font-bold mb-6">
              Your Crypto Growth, Mastered.
            </h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-6">
              Efficiently track, analyze, and optimize your entire crypto
              portfolio with our intuitive, security-first dashboard.
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                <span className="block text-cyan-400 font-bold text-2xl">
                  $81k+
                </span>
                <span className="text-xs text-gray-500 uppercase">
                  Tracked Value
                </span>
              </div>
              <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                <span className="block text-emerald-400 font-bold text-2xl">
                  Live
                </span>
                <span className="text-xs text-gray-500 uppercase">
                  Data Points
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Phone with YOUR image */}
        <div className="relative flex justify-center items-center">
          {/* Outer Glow */}
          <div className="absolute w-[350px] h-[350px] bg-cyan-500/20 blur-[100px] rounded-full" />

          {/* Smartphone Frame */}
          <div className="relative w-[300px] h-[610px] bg-[#020306] border-[12px] border-[#1a1c24] rounded-[3.5rem] shadow-2xl overflow-hidden ring-1 ring-white/20">
            {/* Notch */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-7 bg-[#1a1c24] rounded-b-2xl z-30" />

            {/* Screen Content - This is where your image goes */}
            <div className="absolute inset-0 z-20 overflow-hidden bg-[#080a0f]">
              <img
                src={mobileDashboardImg}
                alt="Mobile Dashboard"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Bento Grid Features */}
      <section className="px-6 py-24 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-8 rounded-[2rem] border border-white/10 bg-white/5 hover:bg-white/10 transition-all">
            <ShieldCheck className="text-cyan-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Secure & Private</h3>
            <p className="text-gray-400 text-sm">
              We never store your keys. Your data is yours alone.
            </p>
          </div>
          <div className="p-8 rounded-[2rem] border border-white/10 bg-white/5 hover:bg-white/10 transition-all">
            <LineChart className="text-indigo-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Advanced Analytics</h3>
            <p className="text-gray-400 text-sm">
              Deep dive into your portfolio performance over time.
            </p>
          </div>
          <div className="p-8 rounded-[2rem] border border-white/10 bg-white/5 hover:text-white transition-all">
            <Globe className="text-emerald-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Multi-Chain Support</h3>
            <p className="text-gray-400 text-sm">
              Every token on every chain, visualized in one place.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-8 py-12 border-t border-white/5 text-center text-gray-600 text-sm">
        © 2026 TOKEN TREE AI. PORTFOLIO MANAGEMENT REIMAGINED.
      </footer>
    </div>
  );
};

export default LandingPage;
