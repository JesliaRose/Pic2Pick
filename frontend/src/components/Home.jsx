// src/components/Home.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const [productName, setProductName] = useState("");
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (productName.trim() === "") return; // Prevent empty submissions

    try {
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_name: productName }),
      });

      if (!response.ok) throw new Error("Failed to fetch results");

      const data = await response.json();
      navigate("/results", { state: { data } }); // Pass data to Results page
    } catch (error) {
      console.error("Error searching for product:", error);
    }
  };

  return (
    <div className="home">
      <h1>Transform Your Shopping Experience with Pic2Pick</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search for product"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default Home;
