import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import pic2picklogo from "../images/pic2picklogo.png";
import amazonlogo from "../images/amazonlogo.png";
import flipkartlogo from "../images/flipkartlogo.png";
import "./productdetailspage.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";

function ProductDetailsPage() {
  const location = useLocation();
  const uploadedImage = location.state?.image;

  return (
    <div className="product-details-page">
      <Link to="/">
        <img
          src={pic2picklogo}
          alt="Website Logo"
          height={"80"}
          className="logo-image"
        />
      </Link>
      <div className="product-image-details">
        {uploadedImage && (
          <div>
            <img
              src={URL.createObjectURL(uploadedImage)}
              alt="Uploaded"
              style={{ maxWidth: "200px", height: "auto" }}
            />
          </div>
        )}
        <div className="product-text">
          <h2>Samsung Galaxy S24 Ultra</h2>
          <p><span><FontAwesomeIcon icon={faThumbsUp} size="xl" style={{color: "#24ad1a",}} /></span> Good Product</p>
        </div>
      </div>

      <div className="product-prices">
        <div className="product-amazon">
          <img
            src={amazonlogo}
            alt="amazon-logo"
            height={"40"}
            className="logo-image"
            />
            <p>₹ 99,799</p>
          <button className="product-buy-button">Buy on Amazon</button>
        </div>

        <div className="product-flipkart">
          <img
            src={flipkartlogo}
            alt="flipkart-logo"
            height={"40"}
            className="logo-image"
            />
            <p>₹ 1,29,999</p>
          <button className="product-buy-button">Buy on Flipkart</button>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailsPage;
