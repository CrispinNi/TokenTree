// src/components/LandingPage.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const LandingPage = () => {
  const [coins, setCoins] = useState([]);

  useEffect(() => {
    const fetchCoins = async () => {
      try {
        const res = await axios.get(
          "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
          {
            headers: {
              "X-CMC_PRO_API_KEY": "YOUR_API_KEY",
            },
            params: { limit: 5, convert: "USD" },
          },
        );
        setCoins(res.data.data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchCoins();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#050816] via-[#0a0f2c] to-[#050816] text-white font-sans">
      {/* NAVBAR */}
      <nav className="flex justify-between items-center px-8 py-4 backdrop-blur-md bg-white/5 border-b border-white/10">
        <h1 className="text-xl font-bold tracking-wide text-cyan-400">
          TokenTree
        </h1>
        <div className="hidden md:flex gap-6 text-sm text-gray-300">
          <a href="#">Home</a>
          <a href="#">Features</a>
          <a href="#">Pricing</a>
          <a href="#">Community</a>
        </div>
        <button className="bg-cyan-400 text-black px-4 py-2 rounded-full font-semibold hover:scale-105 transition">
          Get Started
        </button>
      </nav>

      {/* HERO */}
      <section className="grid md:grid-cols-2 gap-10 items-center px-8 py-20 max-w-7xl mx-auto">
        {/* LEFT */}
        <div>
          <h1 className="text-5xl font-bold leading-tight mb-6">
            MASTER YOUR <br />
            CRYPTO PORTFOLIO, <br />
            <span className="text-cyan-400">SIMPLIFIED.</span>
          </h1>

          <p className="text-gray-400 mb-6">
            Track, analyze, and optimize your crypto assets in one intelligent
            dashboard.
          </p>

          <div className="flex gap-4">
            <button className="bg-cyan-400 text-black px-6 py-3 rounded-full font-semibold hover:scale-105 transition">
              Sign Up Free
            </button>
            <button className="border border-gray-600 px-6 py-3 rounded-full hover:bg-white/10 transition">
              Watch Demo
            </button>
          </div>
        </div>

        {/* RIGHT (Glow Circle UI) */}
        <div className="relative flex justify-center items-center">
          <div className="w-60 h-60 rounded-full bg-cyan-400/20 blur-3xl absolute"></div>
          <div className="w-40 h-40 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/30">
            <span className="text-3xl font-bold">₿</span>
          </div>
        </div>
      </section>

      {/* TRUST LOGOS */}
      <div className="text-center text-gray-500 mb-12">
        Trusted by thousands globally
      </div>

      {/* FEATURES */}
      <section className="px-8 py-16 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          UNMATCHED FEATURES FOR THE SMART INVESTOR
        </h2>

        <div className="grid md:grid-cols-4 gap-6">
          {[
            "Unified Dashboard",
            "Intelligent Tracking",
            "Advanced Analytics",
            "Secure & Private",
          ].map((feature, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-lg hover:shadow-cyan-500/20 hover:shadow-lg transition"
            >
              <h3 className="font-semibold mb-2 text-cyan-400">{feature}</h3>
              <p className="text-gray-400 text-sm">
                Powerful tools to manage your crypto efficiently.
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* LIVE PRICES */}
      <section className="px-8 py-16 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          Live Market Prices
        </h2>

        <div className="grid md:grid-cols-5 gap-6">
          {coins.map((coin) => (
            <div
              key={coin.id}
              className="p-5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-md hover:scale-105 transition"
            >
              <h3 className="font-bold">{coin.symbol}</h3>
              <p className="text-gray-400 text-sm">{coin.name}</p>

              <p className="mt-2 font-semibold">
                ${coin.quote.USD.price.toFixed(2)}
              </p>

              <p
                className={
                  coin.quote.USD.percent_change_24h > 0
                    ? "text-green-400"
                    : "text-red-400"
                }
              >
                {coin.quote.USD.percent_change_24h.toFixed(2)}%
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* TOOLS SECTION */}
      <section className="px-8 py-16 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">
          POWERFUL TOOLS AT YOUR FINGERTIPS
        </h2>

        <div className="grid md:grid-cols-4 gap-6">
          {[
            "Market Insights",
            "Tax Reporting",
            "API Support",
            "Mobile App",
          ].map((tool, i) => (
            <div
              key={i}
              className="p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition"
            >
              <h3 className="font-semibold text-cyan-400">{tool}</h3>
            </div>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="text-center py-8 border-t border-white/10 text-gray-500">
        © 2026 TokenTree. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;
