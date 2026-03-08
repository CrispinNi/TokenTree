import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import NewsCard from "../components/NewsCard";
import api from "../api/client";

export default function DashboardPage() {
  const [summary, setSummary] = useState({ total_usd_value: 0, per_token: [] });
  const [chartData, setChartData] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [summaryRes, chartRes, newsRes] = await Promise.all([
          api.get("/summary"),
          api.get("/charts"),
          api.get("/news"),
        ]);
        setSummary(summaryRes.data);
        setChartData(chartRes.data.timeseries || []);
        setNews(newsRes.data || []);
      } catch (err) {
        console.error(err);
        setError(
          err.response?.status === 401
            ? "Session expired. Please log in again."
            : "Failed to load data. Please try again.",
        );
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 px-6 sm:px-8 lg:px-12 py-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-4xl font-bold text-white mb-4">Dashboard</h1>
            <p className="text-slate-400 animate-pulse">
              Loading your portfolio...
            </p>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 px-6 sm:px-8 lg:px-12 py-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-4xl font-bold text-white mb-4">Dashboard</h1>
            <div className="bg-red-900/20 border border-red-700 rounded-xl p-4 text-red-400">
              {error}
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="flex-1">
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
          <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 py-10 flex flex-col gap-10">
            {/* Header */}
            <section>
              <div className="pb-6 border-b border-slate-700/50">
                <h1 className="text-4xl font-bold text-white">Dashboard</h1>

                <p className="text-slate-400 text-lg mt-2">
                  Track and manage your crypto portfolio in real-time
                </p>
              </div>
            </section>

            {/* Summary Cards */}
            <section>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
                {/* Total Portfolio Value */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 shadow-xl border border-slate-700 hover:border-blue-500/50 transition-all duration-300">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-2">
                        Total Portfolio Value
                      </p>
                      <p className="text-4xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">
                        ${summary.total_usd_value.toFixed(2)}
                      </p>
                    </div>
                    <div className="text-4xl">💰</div>
                  </div>
                </div>

                {/* Assets */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 shadow-xl border border-slate-700 hover:border-purple-500/50 transition-all duration-300">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-2">
                        Total Assets
                      </p>
                      <p className="text-4xl font-bold text-transparent bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text">
                        {summary.per_token.length}
                      </p>
                    </div>
                    <div className="text-4xl">📊</div>
                  </div>
                </div>

                {/* Data Points */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 shadow-xl border border-slate-700 hover:border-green-500/50 transition-all duration-300">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-2">
                        Price Data Points
                      </p>
                      <p className="text-4xl font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text">
                        {chartData.length}
                      </p>
                    </div>
                    <div className="text-4xl">📈</div>
                  </div>
                </div>
              </div>
            </section>

            {/* Tokens Section */}
            <section>
              {summary.per_token.length > 0 && (
                <div>
                  <h2 className="text-2xl font-bold text-white mb-8">
                    Your Holdings
                  </h2>

                  <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl overflow-hidden shadow-xl border border-slate-700">
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead className="bg-slate-900/50 border-b border-slate-700">
                          <tr>
                            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">
                              Symbol
                            </th>
                            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-300">
                              Quantity
                            </th>
                            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-300">
                              Price (USD)
                            </th>
                            <th className="px-6 py-4 text-right text-sm font-semibold text-slate-300">
                              Total Value
                            </th>
                          </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-700">
                          {summary.per_token.map((t) => (
                            <tr
                              key={t.id}
                              className="hover:bg-slate-800/50 transition-colors"
                            >
                              <td className="px-6 py-4 text-white font-semibold">
                                {t.symbol}
                              </td>

                              <td className="px-6 py-4 text-right text-slate-300">
                                {t.quantity.toFixed(8)}
                              </td>

                              <td className="px-6 py-4 text-right text-slate-400">
                                ${t.price_usd.toFixed(2)}
                              </td>

                              <td className="px-6 py-4 text-right text-blue-400 font-semibold">
                                ${t.value_usd.toFixed(2)}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* Empty Portfolio */}
              {summary.per_token.length === 0 && (
                <div className="bg-gradient-to-br from-blue-900/20 to-purple-900/20 rounded-2xl p-10 text-center border border-slate-700">
                  <p className="text-slate-300 text-lg mb-4">
                    No tokens yet. Start building your portfolio!
                  </p>

                  <a
                    href="/add-crypto"
                    className="inline-block bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-blue-500/50"
                  >
                    Add Your First Crypto
                  </a>
                </div>
              )}
            </section>

            {/* Trending News */}
            <div>
              <div className="flex items-center justify-between mb-8 pb-8 border-b border-slate-700/50">
                <div>
                  <h2 className="text-2xl font-bold text-white">
                    📰 Trending News
                  </h2>

                  <p className="text-slate-400 text-sm mt-1">
                    Latest cryptocurrency updates and market trends
                  </p>
                </div>
              </div>

              {news.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                  {news.map((item) => (
                    <NewsCard key={item.url} item={item} />
                  ))}
                </div>
              ) : (
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-12 text-center border border-slate-700">
                  <p className="text-slate-400 text-lg">
                    No news available right now. Check back later!
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
