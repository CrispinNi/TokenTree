import { useState } from "react";
import Navbar from "../components/Navbar";
import api from "../api/client";

export default function AddCryptoPage() {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/tokens", {
        symbol,
        quantity: Number(quantity),
      });
      setSymbol("");
      setQuantity("");
      alert("Token added!");
    } catch (err) {
      console.error(err);
      alert("Failed to add token.");
    }
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">
              Add Cryptocurrency
            </h1>
            <p className="text-slate-400">
              Expand your portfolio with new crypto assets
            </p>
          </div>

          {/* Form Card */}
          <div className="bg-gradient-to-b from-slate-800 to-slate-900 rounded-2xl p-8 shadow-2xl border border-slate-700">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Coin Symbol Input */}
              <div>
                <label className="block text-slate-300 font-semibold mb-3">
                  Cryptocurrency Symbol
                </label>
                <input
                  type="text"
                  placeholder="e.g., bitcoin, ethereum, cardano"
                  className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all duration-200"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  required
                />
                <p className="text-slate-500 text-sm mt-2">
                  Enter the coin name or symbol (e.g., BTC, ETH)
                </p>
              </div>

              {/* Quantity Input */}
              <div>
                <label className="block text-slate-300 font-semibold mb-3">
                  Quantity
                </label>
                <input
                  type="number"
                  placeholder="0.00"
                  step="0.00000001"
                  className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all duration-200"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  required
                />
                <p className="text-slate-500 text-sm mt-2">
                  How many coins do you own?
                </p>
              </div>

              {/* Buttons */}
              <div className="flex gap-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-blue-500/50"
                >
                  Add to Portfolio
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSymbol("");
                    setQuantity("");
                  }}
                  className="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition-all duration-200"
                >
                  Clear
                </button>
              </div>
            </form>
          </div>

          {/* Info Section */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700">
              <h3 className="text-white font-semibold text-lg mb-3">
                💡 Pro Tip
              </h3>
              <p className="text-slate-400 text-sm">
                Use the full coin name or symbol. Our system will fetch
                real-time price data for your portfolio tracking.
              </p>
            </div>
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700">
              <h3 className="text-white font-semibold text-lg mb-3">
                📊 Real-time Updates
              </h3>
              <p className="text-slate-400 text-sm">
                Your portfolio value updates automatically based on current
                market prices.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
