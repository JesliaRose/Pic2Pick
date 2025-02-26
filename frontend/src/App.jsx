/* import React from 'react';
import ProductSearch from './components/ProductSearch';

const App = () => {
  return (
    <div>
      <ProductSearch />
    </div>
  );
};

export default App;
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ProductDetailsPage from './components/ProductDetailsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/product" element={<ProductDetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;