import Navbar from "../components/Navbar";

export default function DashboardPage() {
  return (
    <>
      <Navbar />
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white p-4 shadow rounded">💰 Total USD Value</div>
          <div className="bg-white p-4 shadow rounded">📊 Chart 1</div>
          <div className="bg-white p-4 shadow rounded">📈 Chart 2</div>
          <div className="bg-white p-4 shadow rounded col-span-3">
            📰 Trending News
          </div>
        </div>
      </div>
    </>
  );
}
