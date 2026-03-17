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
  Mobile, // Assuming you might have a mobile icon or can import one. Otherwise use an icon that fits.
} from "lucide-react";

const CryptoLandingPage = () => {
  return (
    // Replaced solid background with the requested gradient, and removed any extra borders on the page container.
    <div className="min-h-screen bg-gradient-to-br from-[#050816] via-[#0a0f2c] to-[#050816] text-white font-sans selection:bg-cyan-500/30">
      {/* Background Glows (kept subtle) */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[10%] right-[-5%] w-[30%] h-[30%] bg-cyan-500/10 blur-[120px] rounded-full" />
      </div>

      {/* Navbar (removed background/borders as implied by 'remove board for the page contain') */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto bg-transparent">
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

      {/* NEW Section (replacing the Trusted By Section) */}
      <section className="px-6 py-24 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        {/* Left Card (Words) */}
        <div className="p-10 rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/10 to-transparent backdrop-blur-xl group hover:border-cyan-500/50 transition-all duration-300">
          <div className="flex gap-6 items-center mb-8">
            <div className="w-14 h-14 bg-cyan-500/20 rounded-xl flex items-center justify-center text-cyan-400 shrink-0">
              <PieChart size={32} />
            </div>
            <h2 className="text-3xl md:text-4xl font-bold group-hover:text-cyan-400 transition-colors">
              Intuitive Portfolio Control
            </h2>
          </div>
          <p className="text-gray-300 text-lg leading-relaxed mb-6">
            Say goodbye to managing multiple spreadsheets and disparate wallet
            apps. CRYPTOTRACK AI aggregates all your holding into one clear,
            real-time dashboard.
          </p>
          <ul className="text-gray-400 space-y-4 list-disc list-inside">
            <li>Sync over 50+ blockchains instantly</li>
            <li>Monitor performance history and PnL</li>
            <li>Get deep insights into asset allocation</li>
            <li>Identify your best and worst performers</li>
          </ul>
        </div>

        {/* Right Card (Dashboard Image on Phone) */}
        <div className="flex justify-center md:justify-end items-center">
          {/* Phone Frame */}
          <div className="relative w-[300px] h-[600px] bg-[#020306] border-[14px] border-[#1a1c24] rounded-[3rem] shadow-2xl shadow-cyan-500/10 overflow-hidden transform md:rotate-3">
            {/* Front Camera/Notch Area */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-28 h-7 bg-[#1a1c24] rounded-b-2xl z-20" />

            {/* Screen Content (the provided image) */}
            <div className="absolute inset-0 bg-[#080a0f] z-10 flex flex-col p-4 pt-10">
              <img
                src="/path/to/your/image_0.png" // !!! IMPORTANT: Replace this with the actual path to your image !!!
                alt="CryptoTrack AI Dashboard Mobile View"
                className="w-full h-full object-cover object-top rounded-t-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Bento Grid Features (unchanged) */}
      <section className="px-6 py-24 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Unmatched Features for the Smart Investor
          </h2>
          <div className="w-20 h-1 bg-cyan-500 mx-auto rounded-full"></div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Main Card (using the same style as the new left card) */}
          <div className="md:col-span-2 md:row-span-2 group relative p-8 rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/10 to-transparent backdrop-blur-xl overflow-hidden hover:border-cyan-500/50 transition-all duration-300">
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

      {/* Footer / Final CTA (background-removed) */}
      <footer className="px-6 py-12 max-w-7xl mx-auto border-t border-white/5 bg-transparent flex flex-col md:flex-row justify-between items-center gap-6">
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

export default CryptoLandingPage;
