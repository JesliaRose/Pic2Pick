import React, { useState } from "react";
import axios from "axios";

const ProductSearch = () => {
  const [productName, setProductName] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:5000/api/search",
        { product_name: productName }
      );
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Product Price Comparison</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter product name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      {loading && <p>Loading...</p>}

      {results && (
        <div>
          <h2>Results</h2>

          <div>
            <h3>Flipkart</h3>
            <p>Title: {results.flipkart.title}</p>
            <p>Price: {results.flipkart.price}</p>
            <a href={results.flipkart.url} target="_blank" rel="noreferrer">
              View on Flipkart
            </a>
          </div>

          <div>
            <h3>Amazon</h3>
            <p>Title: {results.amazon.title}</p>
            <p>Price: {results.amazon.price}</p>
            <a href={results.amazon.url} target="_blank" rel="noreferrer">
              View on Amazon
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductSearch;
