import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import NewsCard from "../components/NewsCard";
import api from "../api/client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export default function DashboardPage() {
  const [summary, setSummary] = useState({ total_usd_value: 0, per_token: [] });
  const [chartData, setChartData] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const COLORS = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"];

  useEffect(() => {
    const load = async () => {
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
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
          Loading dashboard...
        </div>
      </>
    );
  }

  const allocationData = summary.per_token.map((t) => ({
    name: t.symbol,
    value: t.value_usd,
  }));

  const movers = summary.per_token.slice(0, 4).map((t) => ({
    symbol: t.symbol,
    price: t.price_usd,
    change: (Math.random() * 10 - 5).toFixed(2),
  }));

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
                  Track and manage your crypto portfolio
                </p>
              </div>
            </section>

            {/* Summary Cards */}
            <section>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700">
                  <p className="text-slate-400 text-sm">Portfolio Value</p>
                  <p className="text-4xl font-bold text-blue-400">
                    ${summary.total_usd_value.toFixed(2)}
                  </p>
                </div>

                <div
                  onClick={() => setShowModal(true)}
                  className="bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700 cursor-pointer hover:border-purple-500 hover:shadow-lg hover:shadow-purple-500/20 transition-all duration-200"
                >
                  <p className="text-slate-400 text-sm">Total Assets</p>
                  <p className="text-4xl font-bold text-purple-400">
                    {summary.per_token.length}
                  </p>
                  <p className="text-slate-500 text-xs mt-2">
                    Click to view holdings
                  </p>
                </div>

                <div className="bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700">
                  <p className="text-slate-400 text-sm">Data Points</p>
                  <p className="text-4xl font-bold text-green-400">
                    {chartData.length}
                  </p>
                </div>
              </div>
            </section>

            {/* Charts Section */}
            <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Portfolio Performance */}
              <div className="lg:col-span-2 bg-slate-800 p-6 rounded-2xl border border-slate-700">
                <h2 className="text-white font-semibold mb-4">
                  📈 Portfolio Performance
                </h2>

                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={chartData}>
                    <XAxis dataKey="time" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="value"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {/* Allocation Chart */}
              <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700">
                <h2 className="text-white font-semibold mb-4">
                  Portfolio Allocation
                </h2>

                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={allocationData}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={100}
                      label
                    >
                      {allocationData.map((entry, index) => (
                        <Cell
                          key={index}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </section>

            {/* Market Movers */}
            <section>
              <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700">
                <h2 className="text-white font-semibold mb-6">
                  🔥 Market Movers
                </h2>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  {movers.map((coin) => (
                    <div
                      key={coin.symbol}
                      className="bg-slate-900 p-4 rounded-xl text-center"
                    >
                      <p className="text-white font-semibold">{coin.symbol}</p>

                      <p className="text-slate-400 text-sm">
                        ${coin.price.toFixed(2)}
                      </p>

                      <p
                        className={
                          coin.change > 0 ? "text-green-400" : "text-red-400"
                        }
                      >
                        {coin.change}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* News */}
            <section>
              <h2 className="text-2xl font-bold text-white mb-6">
                📰 Crypto News
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                {news.map((item) => (
                  <NewsCard key={item.url} item={item} />
                ))}
              </div>
            </section>
          </div>
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 max-w-4xl w-full max-h-[90vh] overflow-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-slate-900 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
              <h3 className="text-2xl font-bold text-white">Your Holdings</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-white text-2xl leading-none"
              >
                ✕
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="px-4 py-3 text-left text-slate-300">
                      Symbol
                    </th>
                    <th className="px-4 py-3 text-right text-slate-300">
                      Quantity
                    </th>
                    <th className="px-4 py-3 text-right text-slate-300">
                      Price
                    </th>
                    <th className="px-4 py-3 text-right text-slate-300">
                      Value
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {summary.per_token.map((t) => (
                    <tr
                      key={t.id}
                      className="border-b border-slate-700 hover:bg-slate-700/30"
                    >
                      <td className="px-4 py-3 text-white font-semibold">
                        {t.symbol}
                      </td>
                      <td className="px-4 py-3 text-right text-slate-300">
                        {t.quantity.toFixed(6)}
                      </td>
                      <td className="px-4 py-3 text-right text-slate-400">
                        ${t.price_usd.toFixed(2)}
                      </td>
                      <td className="px-4 py-3 text-right text-blue-400 font-semibold">
                        ${t.value_usd.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {summary.per_token.length === 0 && (
                <p className="text-center text-slate-400 py-8">
                  No holdings yet
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
