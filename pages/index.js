// pages/index.js (or any other component)

// import { useState, useEffect } from 'react';

// const HomePage = () => {
//   const [productTitles, setProductTitles] = useState([]);

//   useEffect(() => {
//     // Fetch data from the API route
//     fetch('/api/scraper')
//       .then((response) => response.json())
//       .then((data) => {
//         setProductTitles(data.productTitles);
//       })
//       .catch((error) => console.error(error));
//   }, []);

//   return (
//     <div>
//       <h1>Urban Outfitters Products:</h1>
//       <ul>
//         {productTitles.map((title, index) => (
//           <li key={index}>{title}</li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default HomePage;

import { useState, useEffect } from 'react';

const HomePage = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // Fetch data from the API route
    fetch('/api/scraper')
      .then((response) => response.json())
      .then((data) => {
        setProducts(data.products);
      })
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h1>Urban Outfitters Products:</h1>
      <ul>
        {products.map((product, index) => (
          <li key={index}>
            <h3>{product.title}</h3>
            <img src={product.image} alt={product.title} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HomePage;


