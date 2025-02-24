import React, { useState } from 'react';
import axios from 'axios';

const ProductSearch = () => {
  const [productName, setProductName] = useState('');
  const [image, setImage] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleProductNameChange = (e) => {
    setProductName(e.target.value);
  };

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('product_name', productName);
    if (image) {
      formData.append('image', image);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/search', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResults(response.data);
    } catch (err) {
      setError('Failed to fetch product data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Pic2Pick: Compare Prices</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Product Name:
          <input type="text" value={productName} onChange={handleProductNameChange} />
        </label>
        <label>
          Upload Image:
          <input type="file" onChange={handleImageChange} />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {results && (
        <div className="results">
          <h2>Search Results for: {results.search_query}</h2>

          <div className="result">
            <h3>Flipkart</h3>
            <p>Price: {results.flipkart.price}</p>
            <a href={results.flipkart.url} target="_blank" rel="noopener noreferrer">
              View on Flipkart
            </a>
          </div>

          <div className="result">
            <h3>Amazon</h3>
            <p>Price: {results.amazon.price}</p>
            <a href={results.amazon.url} target="_blank" rel="noopener noreferrer">
              View on Amazon
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductSearch;
