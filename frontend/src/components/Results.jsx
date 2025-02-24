import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { data } = location.state || {};

  if (!data) {
    return <p>No data found. Please go back and search for a product.</p>;
  }

  return (
    <div className="container">
      <h1>Price Comparison</h1>
      <h2>Results for: {data.product_name}</h2>

      <div className="result">
        <h3>Amazon</h3>
        <p>Price: {data.amazon_price}</p>
        <a href={data.amazon_link} target="_blank" rel="noopener noreferrer">
          Buy on Amazon
        </a>
      </div>

      <div className="result">
        <h3>Flipkart</h3>
        <p>Price: {data.flipkart_price}</p>
        <a href={data.flipkart_link} target="_blank" rel="noopener noreferrer">
          Buy on Flipkart
        </a>
      </div>

      <button onClick={() => navigate('/')}>Back to Search</button>
    </div>
  );
};

export default Results;
