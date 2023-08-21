import React, { useState, useEffect } from "react";
import styles from "./Home.module.css";
import Link from "next/link";
import Filter from "../Filter/Filter";
import Image from "next/image";
import BM from "../../public/BM.svg";
import S from "../../public/S.svg";

function HomePage() {
  const [data, setData] = useState([]);

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

  return (
    <div>
      <div>
        <Image className={styles.logo} src={BM} />
        <Image className={styles.logo} src={S} />
      </div>
      <h1 className={styles.topBar}>Search...</h1>
      <div className={styles.container}>
        <Filter />

        <div className={styles.grid}>
          {data.map((item) => (
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
