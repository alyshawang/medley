// // pages/api/scrape.js

// import { spawn } from 'child_process';

// export default async function handler(req, res) {
//   try {
//     // Run the Python script using child_process
//     const pythonProcess = spawn('python', ['/Users/alyshawang/Documents/brandy2/nextjs-blog/web_scraping.py']);

//     pythonProcess.stdout.on('data', (data) => {
//       // Handle the data received from the Python script (product titles)
//       const productTitles = data.toString().trim().split('\n');
//       res.status(200).json({ productTitles });
//     });

//     pythonProcess.stderr.on('data', (data) => {
//       // Handle errors if any
//       console.error(data.toString());
//       res.status(500).json({ error: 'Error occurred during scraping' });
//     });
//   } catch (error) {
//     console.error(error);
//     res.status(500).json({ error: 'Internal server error' });
//   }
// }
