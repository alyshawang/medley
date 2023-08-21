import React, { useState } from "react";
import styles from "./Filter.module.css";

function FilterBar() {
  const [selectedOption, setSelectedOption] = useState(""); // state to store the selected option

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value); // update the selected option when it changes
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
          <option value="option1">Option 1</option>
          <option value="option2">Option 2</option>
        </select>
      </div>
      {/* Dropdown menu */}
      <div>
        <div className={styles.filter}>
          <label htmlFor="filterDropdown">FILTER</label>
          <br></br>
          <select
            id="filterDropdown"
            value={selectedOption}
            onChange={handleOptionChange}
            className={styles.customDropdown}
          >
            <option className={styles.dropdown} value="">
              Brand
            </option>
            <option value="option1">Brandy Melville</option>
            <option value="option2">Stussy</option>
          </select>
          <br></br>

          <select
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
          <br></br>

          <select
            id="filterDropdown"
            value={selectedOption}
            onChange={handleOptionChange}
            className={styles.customDropdown}
          >
            <option className={styles.dropdown} value="">
              Price Range
            </option>
            <option value="option1">Brandy Melville</option>
            <option value="option2">Stussy</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default FilterBar;
