import React from "react";
import {
  Wallet,
  LineChart,
  ShieldCheck,
  PieChart,
  ArrowUpRight,
  Layers,
  Zap,
  Globe,
} from "lucide-react";

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-[#080a0f] text-white font-sans selection:bg-cyan-500/30">
      {/* Background Glows */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[10%] right-[-5%] w-[30%] h-[30%] bg-cyan-500/10 blur-[120px] rounded-full" />
      </div>

      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
            <Layers size={24} className="text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">
            CRYPTO<span className="text-cyan-400">TRACK</span> AI
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
          <a href="#" className="hover:text-white transition-colors">
            Home
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Features
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Security
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Pricing
          </a>
        </div>

        <button className="bg-cyan-500/10 border border-cyan-500/50 text-cyan-400 px-6 py-2 rounded-full text-sm font-semibold hover:bg-cyan-500 hover:text-white transition-all duration-300">
          Get Started
        </button>
      </nav>

      {/* Hero Section */}
      <header className="px-6 pt-20 pb-16 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 text-xs text-cyan-300 mb-6 animate-fade-in">
          <Zap size={14} />
          <span>v2.0 is now live with Multi-Chain Support</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-gradient-to-b from-white to-gray-500 bg-clip-text text-transparent">
          MASTER YOUR <br /> CRYPTO PORTFOLIO, <br /> SIMPLIFIED.
        </h1>
        <p className="text-gray-400 text-lg md:text-xl mb-10 max-w-2xl mx-auto leading-relaxed">
          Effortlessly track, analyze, and optimize all your crypto assets in
          one intuitive dashboard. Real-time updates, security-first approach.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button className="w-full sm:w-auto px-8 py-4 bg-cyan-500 rounded-xl font-bold text-black hover:bg-cyan-400 hover:scale-105 transition-all shadow-xl shadow-cyan-500/20">
            Sign Up Free
          </button>
          <button className="w-full sm:w-auto px-8 py-4 bg-white/5 border border-white/10 rounded-xl font-bold hover:bg-white/10 transition-all">
            Watch Demo
          </button>
        </div>
      </header>

      {/* Trusted By Section */}
      <section className="py-12 border-y border-white/5 bg-white/[0.01]">
        <p className="text-center text-gray-500 text-xs uppercase tracking-[0.2em] mb-8">
          Trusted by thousands globally
        </p>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-40 grayscale">
          <span className="text-2xl font-bold">Forbes</span>
          <span className="text-2xl font-bold">TechCrunch</span>
          <span className="text-2xl font-bold">CoinDesk</span>
          <span className="text-2xl font-bold">Bloomberg</span>
        </div>
      </section>

      {/* Bento Grid Features */}
      <section className="px-6 py-24 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Unmatched Features for the Smart Investor
          </h2>
          <div className="w-20 h-1 bg-cyan-500 mx-auto rounded-full"></div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Main Card */}
          <div className="md:col-span-2 md:row-span-2 group relative p-8 rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/10 to-transparent backdrop-blur-xl overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
              <PieChart size={120} />
            </div>
            <div className="relative z-10 h-full flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center text-cyan-400 mb-6">
                  <Wallet size={28} />
                </div>
                <h3 className="text-2xl font-bold mb-4">Unified Dashboard</h3>
                <p className="text-gray-400 leading-relaxed">
                  Connect all wallets & exchanges. Get a birds-eye view of your
                  total net worth, profit/loss, and asset allocation across 50+
                  blockchains.
                </p>
              </div>
              <div className="mt-8 pt-6 border-t border-white/5">
                <div className="flex justify-between text-sm text-gray-500">
                  <span>Supported Exchanges</span>
                  <span className="text-white font-mono">24/24 Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Card 2 */}
          <div className="md:col-span-2 p-8 rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all border-l-indigo-500/50 border-l-2">
            <div className="flex gap-6 items-start">
              <div className="w-12 h-12 bg-indigo-500/20 rounded-lg flex items-center justify-center text-indigo-400 shrink-0">
                <LineChart size={28} />
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2">Intelligent Tracking</h3>
                <p className="text-gray-400 text-sm">
                  Monitor PnL, track gas fees, and track DeFi yields
                  automatically.
                </p>
              </div>
            </div>
          </div>

          {/* Card 3 */}
          <div className="md:col-span-1 p-8 rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all">
            <div className="w-12 h-12 bg-emerald-500/20 rounded-lg flex items-center justify-center text-emerald-400 mb-6">
              <ShieldCheck size={28} />
            </div>
            <h3 className="text-xl font-bold mb-2">Secure & Private</h3>
            <p className="text-gray-400 text-sm">
              Zero-knowledge encryption. We never store your keys.
            </p>
          </div>

          {/* Card 4 */}
          <div className="md:col-span-1 p-8 rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all">
            <div className="w-12 h-12 bg-amber-500/20 rounded-lg flex items-center justify-center text-amber-400 mb-6">
              <Globe size={28} />
            </div>
            <h3 className="text-xl font-bold mb-2">Multi-Chain</h3>
            <p className="text-gray-400 text-sm">
              Native support for ETH, SOL, BTC, and more.
            </p>
          </div>
        </div>
      </section>

      {/* Footer / Final CTA */}
      <footer className="px-6 py-12 max-w-7xl mx-auto border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="text-gray-500 text-sm">
          © 2026 CRYPTOTRACK AI. All rights reserved.
        </div>
        <div className="flex gap-6 text-gray-400 text-sm">
          <a href="#" className="hover:text-white transition-colors">
            Twitter
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Discord
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Terms
          </a>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
