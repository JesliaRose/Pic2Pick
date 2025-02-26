import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

function ProductDetailsPage() {
  const location = useLocation();
  const uploadedImage = location.state?.image;

  return (
    <div>
      <div>
        <h1>Product Page</h1>
        {uploadedImage && (
          <div>
            <h2>Uploaded Image:</h2>
            <img
              src={URL.createObjectURL(uploadedImage)}
              alt="Uploaded"
              style={{ maxWidth: "50%", height: "auto" }}
            />
          </div>
        )}
      </div>
      <div className="product-details-page">
        <h1>Pic2Pick</h1>
        <h2>Samsung Galaxy S24 Ultra</h2>
        <p>Good Product</p>
        <div className="prices">
          <span>Amazon: ₹99,799</span>
          <span>Flipkart: ₹1,31,999</span>
        </div>
        <div className="buttons">
          <button>Buy on Amazon</button>
          <button>Buy on Flipkart</button>
        </div>
        <Link to="/">
          <button className="back-to-home-button">Back to Home</button>
        </Link>
      </div>
    </div>
  );
}

export default ProductDetailsPage;
