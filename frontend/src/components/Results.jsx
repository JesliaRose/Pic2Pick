import "./Results.css"

const Results = ({ productData }) => {
  if (!productData) return <div>Loading...</div>;

  const {
    search_query,
    flipkart_title,
    flipkart_price,
    flipkart_url,
    amazon_price,
    amazon_link,
  } = productData;

  return (
    <div className="results">
      <header className="logo">Pic<span>2</span>Pick</header>
      <div className="product-card">
        <h2>{search_query}</h2>
        <p>✅ Good Product</p>
        <div className="price-container">
          <div className="price-box amazon">
            <h3>Amazon</h3>
            <p>₹ {amazon_price || "Not Found"}</p>
            <a href={amazon_link} target="_blank" rel="noopener noreferrer">
              Buy on Amazon
            </a>
          </div>
          <div className="price-box flipkart">
            <h3>Flipkart</h3>
            <p>₹ {flipkart_price || "Not Found"}</p>
            <a href={flipkart_url} target="_blank" rel="noopener noreferrer">
              Buy on Flipkart
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
