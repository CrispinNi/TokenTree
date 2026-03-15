import React, { useEffect, useState } from "react";
import axios from "axios";

const LandingPage = () => {
  const [coins, setCoins] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCoins = async () => {
      try {
        const response = await axios.get(
          "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
          {
            headers: {
              "X-CMC_PRO_API_KEY": "2a190483acb1475d80f2b18deb042d82", // replace with your API key
            },
            params: {
              start: 1,
              limit: 5,
              convert: "USD",
            },
          },
        );
        setCoins(response.data.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching coin data:", error);
        setLoading(false);
      }
    };

    fetchCoins();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Hero Section */}
      <section className="text-center py-20 px-4">
        <h1 className="text-5xl font-bold mb-4">TokenTree</h1>
        <p className="text-lg mb-8">
          Track, manage, and grow your crypto portfolio effortlessly.
        </p>
        <a
          href="/login"
          className="bg-green-500 hover:bg-green-600 text-black px-6 py-3 rounded-lg font-semibold transition"
        >
          Get Started
        </a>
      </section>

      {/* Live Crypto Prices */}
      <section id="coins" className="py-12 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-center">
          Live Crypto Prices
        </h2>
        {loading ? (
          <p className="text-center">Loading...</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
            {coins.map((coin) => (
              <div
                key={coin.id}
                className="bg-slate-800 p-4 rounded-lg shadow hover:scale-105 transform transition"
              >
                <h3 className="font-bold text-xl mb-2">{coin.name}</h3>
                <p className="text-gray-400">{coin.symbol}</p>
                <p className="mt-2 text-lg font-semibold">
                  ${coin.quote.USD.price.toFixed(2)}
                </p>
                <p
                  className={`mt-1 ${
                    coin.quote.USD.percent_change_24h >= 0
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >
                  {coin.quote.USD.percent_change_24h.toFixed(2)}%
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-slate-900">
        <h2 className="text-3xl font-bold mb-8 text-center">Why TokenTree?</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="text-center p-4">
            <h3 className="font-semibold text-xl mb-2">Real-Time Tracking</h3>
            <p>Stay updated with the latest market prices and trends.</p>
          </div>
          <div className="text-center p-4">
            <h3 className="font-semibold text-xl mb-2">Portfolio Insights</h3>
            <p>Analyze your holdings and make informed decisions.</p>
          </div>
          <div className="text-center p-4">
            <h3 className="font-semibold text-xl mb-2">Secure & Private</h3>
            <p>Your portfolio data is safe and only accessible by you.</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 text-center text-gray-400 border-t border-slate-700">
        © 2026 TokenTree. All rights reserved.
      </footer>
    </div>
  );
};

export default LandingPage;
