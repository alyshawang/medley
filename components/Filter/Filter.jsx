import React, { useState } from "react";
import styles from "./Filter.module.css";

function FilterBar({ onSortChange, onBrandChange, onPriceRangeChange }) {
  const [selectedOption, setSelectedOption] = useState(""); 
  const [selectedBrandOption, setSelectedBrandOption] = useState("");
  const [selectedPriceRange, setSelectedPriceRange] = useState("");

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value); // update the selected option when it changes
    onSortChange(event.target.value); // notify the parent component of the sort change
  };

  const handleBrandChange = (event) => {
    setSelectedBrandOption(event.target.value);
    onBrandChange(event.target.value);
  };

  const handlePriceRangeChange = (event) => {
    setSelectedPriceRange(event.target.value);
    onPriceRangeChange(event.target.value);
  };

  return (
    <div className={styles.sidebar}>
      <style jsx global>{`
        body {
          margin: 0px;
          padding: 0px;
        }
      `}</style>
      <div className={styles.sort}>
        {/* Dropdown menu */}
        <label htmlFor="filterDropdown">SORT</label>
        <br></br>
        <select
          id="filterDropdown"
          value={selectedOption}
          onChange={handleOptionChange}
          className={styles.customDropdown}
        >
          <option value="">By Price</option>
          <option value="lowestToHighest">Lowest to Highest</option>
          <option value="highestToLowest">Highest to Lowest</option>
        </select>
      </div>
      {/* Dropdown menu */}
      <div>
        <div className={styles.filter}>
          <label htmlFor="filterDropdown">FILTER</label>
          <br></br>
          <select
            id="filterDropdown"
            value={selectedBrandOption}
            onChange={handleBrandChange}
            className={styles.customDropdown}
          >
            <option className={styles.dropdown} value="">
              Brand
            </option>
            <option value="Brandy Melville">Brandy Melville</option>
            <option value="Stussy">STUSSY</option>
          </select>
          <br></br>

          {/* <select
            id="filterDropdown"
            value={selectedOption}
            onChange={handleOptionChange}
            className={styles.customDropdown}
          >
            <option className={styles.dropdown} value="">
              Style
            </option>
            <option value="option1">Brandy Melville</option>
            <option value="option2">Stussy</option>
          </select>
          <br></br> */}

          <select
            id="filterDropdown"
            value={selectedPriceRange}
            onChange={handlePriceRangeChange}
            className={styles.customDropdown}
          >
            <option className={styles.dropdown} value="">
              Price Range
            </option>
            <option value="0-20">0-20</option>
            <option value="20-50">20-50</option>
            <option value="50-100">50-100</option>
            <option value="100-300">100+</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default FilterBar;
