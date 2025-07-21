import Navbar from "../components/Navbar";

export default function AddCryptoPage() {
  return (
    <>
      <Navbar />
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-4">Add Cryptocurrency</h1>
        <form className="space-y-4 bg-white p-4 rounded shadow max-w-md">
          <input
            type="text"
            placeholder="Coin Name"
            className="w-full p-2 border rounded"
          />
          <input
            type="number"
            placeholder="Quantity"
            className="w-full p-2 border rounded"
          />
          <input
            type="number"
            placeholder="Buy Price (USD)"
            className="w-full p-2 border rounded"
          />
          <button className="bg-green-500 text-white px-4 py-2 rounded">
            Add
          </button>
        </form>
      </div>
    </>
  );
}
