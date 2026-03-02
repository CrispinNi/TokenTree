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
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-4">Add Cryptocurrency</h1>
        <form
          onSubmit={handleSubmit}
          className="space-y-4 bg-white p-4 rounded shadow max-w-md"
        >
          <input
            type="text"
            placeholder="Coin Symbol (e.g. bitcoin)"
            className="w-full p-2 border rounded"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Quantity"
            className="w-full p-2 border rounded"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
          <button className="bg-green-500 text-white px-4 py-2 rounded">
            Add
          </button>
        </form>
      </div>
    </>
  );
}
