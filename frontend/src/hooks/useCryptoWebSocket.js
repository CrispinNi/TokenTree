import { useEffect, useState } from "react";

export const useCryptoWebSocket = (symbol) => {
  const [price, setPrice] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const ws = new WebSocket(`${protocol}//localhost:8000/ws/price/${symbol}`);

    ws.onopen = () => {
      console.log(`Connected to ${symbol} price stream`);
      setIsConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.symbol) {
          setPrice(data);
        }
      } catch (e) {
        console.error("Error parsing message:", e);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setIsConnected(false);
      setError("WebSocket connection error");
    };

    ws.onclose = () => {
      console.log("Disconnected from price stream");
      setIsConnected(false);
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [symbol]);

  return { price, isConnected, error };
};
