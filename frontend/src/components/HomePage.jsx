// HomePage.jsx
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./homepage.css";
import pic2picklogo from "../images/pic2picklogo.png";
import heroimage from "../images/homepageimage.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

function HomePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (searchQuery.trim()) {
      navigate("/product");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const validTypes = ["image/png", "image/jpeg", "image/jpg"];
      if (!validTypes.includes(file.type)) {
        alert("Please upload a valid PNG or JPEG file.");
        return;
      }
      console.log("Uploaded file:", file);
      navigate("/product", { state: { image: file } });
    }
  };

  return (
    <div className="home-container">
      <div className="left-content">
        <div className="logo-container">
          <img src={pic2picklogo} alt="Website Logo" className="logo-image" />
        </div>

        <div className="main-content">
          <p className="tagline">
            Transform Your Shopping Experience with Pic2Pick - Snap, Compare and
            Pick the Best Deals!
          </p>

          <div className="upload-content">
            <div className="upload-section">
              <input
                type="file"
                id="image-upload"
                accept="image/*"
                style={{ display: "none" }}
                onChange={handleImageUpload}
              />
              <label htmlFor="image-upload" className="upload-button">
                Upload an Image
              </label>
            </div>
            <div className="upload-or-text">
              <p>OR</p>
            </div>
          </div>

          <div className="search-container">
            <div className="input-wrapper">
              <input
                type="text"
                placeholder="Search for products"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={handleKeyPress}
              />
              <button onClick={handleSearch} className="search-button">
                <FontAwesomeIcon
                  icon={faMagnifyingGlass}
                  size="lg"
                  style={{ color: "#f1faee" }}
                />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="right-image">
        <img src={heroimage} alt="Website Logo" className="logo-image" />
      </div>
    </div>
  );
}

export default HomePage;
