import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
  const [productName, setProductName] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

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
      const response = await axios.post('http://127.0.0.1:5000/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Navigate to results page with the data
      navigate('/results', { state: { data: response.data } });
    } catch (err) {
      setError('Failed to fetch product data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Pic2Pick: Snap, Compare, Pick!</h1>
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
    </div>
  );
};

export default Home;
