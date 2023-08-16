import React, { useState, useEffect } from 'react';
import styles from "./index.module.css";
import "./index.module.css";
import Link from 'next/link'; // Import the Link component from Next.js

function HomePage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchDataFromBackend();
  }, []);

  const fetchDataFromBackend = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/data'); // Replace with your Flask API endpoint
      const jsonData = await response.json();
      setData(jsonData); // Set the fetched data to state
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

//   return (
//   <div>
//   <h1>Display Data from Backend</h1>
//   <div className={styles.grid}>
//     {data.map(item => (
//       <div className={styles.item} key={item.image_url}>
//         <img src={item.image_url} alt={item.title} className={styles.image} />
//         <p className={styles.title}>{item.title}</p>
//         <p className={styles.price}>{item.price}</p>
//       </div>
//     ))}
//   </div>
// </div>
// );
// }

return (
  <div>
    <h1>Display Data from Backend</h1>
    <div className={styles.grid}>
      {data.map(item => (
        <div className={styles.item} key={item.image_url}>
          {/* Use the Link component here */}
          <Link href={`${item.link}`} target="_blank">
              <img src={item.image_url} alt={item.title} className={styles.image} />
              <p className={styles.title}>{item.title}</p>
              <p className={styles.price}>{item.price}</p>
          </Link>
        </div>
      ))}
    </div>
  </div>
);
}

export default HomePage;
// // pages/index.js (or any other component)

// // import { useState, useEffect } from 'react';

// // const HomePage = () => {
// //   const [productTitles, setProductTitles] = useState([]);

// //   useEffect(() => {
// //     // Fetch data from the API route
// //     fetch('/api/scraper')
// //       .then((response) => response.json())
// //       .then((data) => {
// //         setProductTitles(data.productTitles);
// //       })
// //       .catch((error) => console.error(error));
// //   }, []);

// //   return (
// //     <div>
// //       <h1>Urban Outfitters Products:</h1>
// //       <ul>
// //         {productTitles.map((title, index) => (
// //           <li key={index}>{title}</li>
// //         ))}
// //       </ul>
// //     </div>
// //   );
// // };

// // export default HomePage;

// import { useState, useEffect } from 'react';

// const HomePage = () => {
//   const [products, setProducts] = useState([]);

//   useEffect(() => {
//     // Fetch data from the API route
//     fetch('/api/scraper')
//       .then((response) => response.json())
//       .then((data) => {
//         setProducts(data.products);
//       })
//       .catch((error) => console.error(error));
//   }, []);

//   return (
//     <div>
//       <h1>Urban Outfitters Products:</h1>
//       <ul>
//         {products.map((product, index) => (
//           <li key={index}>
//             <h3>{product.title}</h3>
//             <img src={product.image} alt={product.title} />
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default HomePage;


