import React, { useState, useEffect } from "react";
import styles from "./Home.module.css";
import Link from "next/link";
import Filter from "../Filter/Filter";
import Image from "next/image";
import BM from "../../public/BM.svg";
import S from "../../public/S.svg";

function HomePage() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState(""); 
  const [sortOption, setSortOption] = useState("");
  const [brandOption, setBrandOption] = useState(""); 
  const [priceRange, setPriceRange] = useState("");

  useEffect(() => {
    fetchDataFromBackend();
  }, []);

  const fetchDataFromBackend = async () => {
    try {
      const response = await fetch("http://localhost:5001/api/data"); // flask API endpoint
      const jsonData = await response.json();
      setData(jsonData); // set the fetched data to state
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  function getPriceColor(price) {
    const numericPrice = parseFloat(price.replace(/[$,]/g, ""));

    if (numericPrice >= 0 && numericPrice < 20) {
      return styles.lowPrice;
    } else if (numericPrice >= 20 && numericPrice < 50) {
      return styles.mediumPrice;
    } else if (numericPrice >= 50 && numericPrice < 100) {
      return styles.highPrice;
    } else {
      return styles.veryHighPrice;
    }
  }

  const filteredData = data.filter((item) =>
    item.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const inputStyles = searchTerm
    ? `${styles.topBar} ${styles.darkText}`
    : styles.topBar;

  const handleSortChange = (value) => {
    setSortOption(value);
  };
  const handleBrandChange = (brand) => {
    setBrandOption(brand);
  };
  const handlePriceRangeChange = (range) => {
    setPriceRange(range);
  };

  let sortedData = [...filteredData];

  if (sortOption === "lowestToHighest") {
    sortedData.sort((a, b) => {
      const priceA = parseFloat(a.price.replace(/[$,]/g, ""));
      const priceB = parseFloat(b.price.replace(/[$,]/g, ""));

      if (!isNaN(priceA) && !isNaN(priceB)) {
        return priceA - priceB;
      } else if (!isNaN(priceA)) {
        return -1;
      } else if (!isNaN(priceB)) {
        return 1;
      } else {
        return 0;
      }
    });
  } else if (sortOption === "highestToLowest") {
    sortedData.sort((a, b) => {
      const priceA = parseFloat(a.price.replace(/[$,]/g, ""));
      const priceB = parseFloat(b.price.replace(/[$,]/g, ""));

      if (!isNaN(priceA) && !isNaN(priceB)) {
        return priceB - priceA;
      } else if (!isNaN(priceA)) {
        return -1;
      } else if (!isNaN(priceB)) {
        return 1;
      } else {
        return 0;
      }
    });
  }

  if (brandOption) {
    sortedData = sortedData.filter((item) => item.brand === brandOption);
  }
  if (priceRange) {
    const [minPrice, maxPrice] = priceRange.split("-");
    sortedData = sortedData.filter((item) => {
      const numericPrice = parseFloat(item.price.replace(/[$,]/g, ""));
      return (
        numericPrice >= parseFloat(minPrice) &&
        numericPrice <= parseFloat(maxPrice)
      );
    });
  }

  return (
    <div>
      <div>
        <Image className={styles.logo} src={BM} />
        <Image className={styles.logo} src={S} />
      </div>
      {/* <h1 className={styles.topBar}>Search...</h1> */}
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className={inputStyles}
      />
      <div className={styles.container}>
        <Filter
          onSortChange={handleSortChange}
          onBrandChange={handleBrandChange}
          onPriceRangeChange={handlePriceRangeChange}
        />

        <div className={styles.grid}>
          {sortedData.map((item) => (
            <div className={styles.item} key={item.image_url}>
              <Link href={`${item.link}`} target="_blank">
                <p className={styles.brand}>{item.brand}</p>
                <p className={styles.title}>{item.title}</p>
                <img
                  src={item.image_url}
                  alt={item.title}
                  className={styles.image}
                />
                <div className={`${styles.priceContainer} `}>
                  <p className={`${styles.price} ${getPriceColor(item.price)}`}>
                    {item.price}
                  </p>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
