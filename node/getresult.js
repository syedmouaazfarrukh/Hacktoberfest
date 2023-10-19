const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();
const port = 3000; 

app.use(express.json());

app.get('/google-search', async (req, res) => {
  const { query } = req.query;

  if (!query) {
    res.status(400).json({ error: 'Missing query parameter' });
    return;
  }

  try {
    const searchUrl = `https://www.google.com/search?q=${query}`;
    const headers = { 'User-Agent': 'Mozilla/5.0' };
    const response = await axios.get(searchUrl, { headers });

    if (response.status === 200) {
      const { data } = response;
      const { title, link } = extractFirstResult(data);

      if (title && link) {
        res.json({ title, link });
      } else {
        res.json({ message: 'No search results found' });
      }
    } else {
      res.status(500).json({ error: 'Failed to retrieve search results' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

function extractFirstResult(searchHtml) {
  const $ = cheerio.load(searchHtml);
  const resultDiv = $('div.tF2Cxc');

  if (resultDiv.length > 0) {
    const title = resultDiv.find('h3').text();
    const link = resultDiv.find('a').attr('href');
    return { title, link };
  }

  return { title: null, link: null };
}

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});


http://localhost:3000/google-search?query=YOUR_QUERY
