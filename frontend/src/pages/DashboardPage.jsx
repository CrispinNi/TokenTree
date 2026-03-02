import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import api from "../api/client";

export default function DashboardPage() {
  const [summary, setSummary] = useState({ total_usd_value: 0, per_token: [] });
  const [chartData, setChartData] = useState([]);
  const [news, setNews] = useState([]);

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
      }
    };
    load();
  }, []);

  return (
    <>
      <Navbar />
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white p-4 shadow rounded">
            <h2 className="font-semibold mb-2">💰 Total USD Value</h2>
            <p className="text-2xl">${summary.total_usd_value.toFixed(2)}</p>
          </div>
          <div className="bg-white p-4 shadow rounded">
            <h2 className="font-semibold mb-2">📊 Tokens</h2>
            <ul className="space-y-1 max-h-64 overflow-auto">
              {summary.per_token.map((t) => (
                <li
                  key={t.id}
                  className="flex justify-between text-sm border-b pb-1"
                >
                  <span>{t.symbol}</span>
                  <span>{t.quantity}</span>
                  <span>${t.value_usd.toFixed(2)}</span>
                </li>
              ))}
              {summary.per_token.length === 0 && (
                <li className="text-sm text-gray-500">
                  No tokens yet. Add some!
                </li>
              )}
            </ul>
          </div>
          <div className="bg-white p-4 shadow rounded">
            <h2 className="font-semibold mb-2">📈 Chart (simple)</h2>
            <div className="text-xs text-gray-600 max-h-64 overflow-auto">
              {chartData.map((series) => (
                <div key={series.symbol} className="mb-2">
                  <div className="font-medium">{series.symbol}</div>
                  <div>
                    {series.prices.slice(-5).map((p, idx) => (
                      <span key={idx} className="mr-1">
                        {p.toFixed(2)}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
              {chartData.length === 0 && (
                <div>No chart data yet (needs valid symbols).</div>
              )}
            </div>
          </div>
          <div className="bg-white p-4 shadow rounded col-span-3">
            <h2 className="font-semibold mb-2">📰 Trending News</h2>
            <ul className="space-y-2 max-h-64 overflow-auto">
              {news.map((item) => (
                <li key={item.url} className="text-sm">
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {item.title}
                  </a>
                  {item.source && (
                    <span className="text-gray-500 ml-2">({item.source})</span>
                  )}
                </li>
              ))}
              {news.length === 0 && (
                <li className="text-sm text-gray-500">
                  No news available right now.
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}
