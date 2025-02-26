import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import pic2picklogo from "../images/pic2picklogo.png";
import amazonlogo from "../images/amazonlogo.png";
import flipkartlogo from "../images/flipkartlogo.png";
import "./productdetailspage.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";

function ProductDetailsPage() {
  const location = useLocation();
  const uploadedImage = location.state?.image;
  const searchQuery = location.state?.searchQuery;

  const [productData, setProductData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProductData = async () => {
      try {
        const formData = new FormData();
        let response;

        if (uploadedImage) {
          formData.append("image", uploadedImage);
          response = await fetch("http://localhost:5000/search", {
            method: "POST",
            body: formData,
          });
        } else if (searchQuery) {
          formData.append("product_name", searchQuery);
          response = await fetch("http://localhost:5000/search", {
            method: "POST",
            body: formData,
          });
        } else {
          throw new Error("No image or search query provided");
        }

        if (!response.ok) throw new Error("Failed to fetch product data");

        const data = await response.json();
        setProductData(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchProductData();
  }, [uploadedImage, searchQuery]);

  if (loading) return (<div className="loading-div"><div className="spinner"></div>Loading...</div>);
  if (error) return <div className="loading-div">Error: {error}</div>;

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
          <h2>
            {productData?.flipkart?.title ||
              productData?.search_query ||
              "Product Name".split(" ")
              .slice(0, 12)
              .join(" ")}
          </h2>
          <p>
            <span>
              <FontAwesomeIcon
                icon={faThumbsUp}
                size="xl"
                style={{ color: "#24ad1a" }}
              />
            </span>{" "}
            Good Product
          </p>
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
          <p>₹{productData?.amazon?.price || "Price not available"}</p>
          <a
            href={productData?.amazon?.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            <button className="product-buy-button">Buy on Amazon</button>
          </a>
        </div>

        <div className="product-flipkart">
          <img
            src={flipkartlogo}
            alt="flipkart-logo"
            height={"40"}
            className="logo-image"
          />
          <p>{productData?.flipkart?.price || "Price not available"}</p>
          <a
            href={productData?.flipkart?.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            <button className="product-buy-button">Buy on Flipkart</button>
          </a>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailsPage;
