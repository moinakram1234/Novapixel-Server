const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const { PythonShell } = require('python-shell');
const axios = require('axios');
const app = express();
const merge = require('deepmerge');
const path = require('path'); // Add this line
const { exec } = require('child_process');

let shopifyoptions = {
  method: 'GET',
  url: 'https://Novapixels.myshopify.com/admin/api/2023-01/products.json',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: {
    username: '75390d7a605fa3053ee913d87b0f1471',
    password: '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'
  }
};

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

function extract_next_page_url(link_header) {
  const links = link_header.split(',');
  for (const link of links) {
    const linkParts = link.split(';');
    if (linkParts.length === 2 && linkParts[1].trim() === 'rel="next"') {
      const url = linkParts[0].trim().slice(1, -1); // Remove the '<' and '>' surrounding the URL
      return url;
    }
  }
  return null;
}
const scriptPath = path.join(__dirname, 'NewProj');
app.get("/", (req, res) => {
  res.send("Welcome to NovaPixel");
});

app.post('/searchlogo', (req, res) => {
  let shopifyapidata = "";
  let pythondata = '';
  let myData = [];
  const inputimage = req.body;

  axios(shopifyoptions)
    .then(function (response) {
      const responseBody = response.data;
      shopifyapidata = responseBody;

      let next_page_url = extract_next_page_url(response.headers.link);

      function fetchNextPage() {
        if (next_page_url) {
          axios
            .get(next_page_url, shopifyoptions)
            .then(function (nextResponse) {
              const nextResponseBody = nextResponse.data;
              shopifyapidata = merge(shopifyapidata, nextResponseBody);

              next_page_url = extract_next_page_url(nextResponse.headers.link);
              fetchNextPage();
            })
            .catch(function (error) {
              console.error(error);
              res.status(500).send('Internal Server Error');
            });
        } else {

        
   exec('pip install opencv-python', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error during pip install: ${error.message}`);
    // Handle the error appropriately
  } else {
    console.log('opencv-python installed successfully');

    // Proceed with your existing code
    const options = {
      mode: 'text',
      pythonOptions: ['-u'],
      scriptPath: scriptPath,
      args: [JSON.stringify(inputimage)]
    };

    const pyshell = new PythonShell('Logo.py', options);
    // Rest of your code
      pyshell.send('Hello, Python!');

          pyshell.on('message', message => {
            pythondata = message;
            myData.push(message);
            console.log(message);
          });

          pyshell.on('error', err => {
            console.error('Python error:', err);
          });

          pyshell.end((err, code, signal) => {
            if (err) {
              console.error('Python script execution failed:', err);
              res.status(500).send('Internal Server Error');
            } else {
              console.log('Python script execution completed with code', code);
              res.send({ shopifyData: shopifyapidata, pythonData: myData });
            }
          });
  
  }
});
        }
      }

      fetchNextPage();
    })
    .catch(function(error) {
      console.error(error);
      res.status(500).send('Internal Server Error');
    });
});

// Call common search model
app.post('/search', (req, res) => {
  let shopifyapidata = "";
  let pythondata = '';
  let myData = [];
  const inputimage = req.body;

  axios(shopifyoptions)
    .then(function (response) {
      const responseBody = response.data;
      shopifyapidata = responseBody;

      let next_page_url = extract_next_page_url(response.headers.link);

      function fetchNextPage() {
        if (next_page_url) {
          axios
            .get(next_page_url, shopifyoptions)
            .then(function (nextResponse) {
              const nextResponseBody = nextResponse.data;
              shopifyapidata = merge(shopifyapidata, nextResponseBody);

              next_page_url = extract_next_page_url(nextResponse.headers.link);
              fetchNextPage();
            })
            .catch(function (error) {
              console.error(error);
              res.status(500).send('Internal Server Error');
            });
        } else {



// Install opencv-python
exec('pip install opencv-python', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error during pip install: ${error.message}`);
    // Handle the error appropriately
  } else {
    console.log('opencv-python installed successfully');

    // Proceed with your existing code
    const options = {
      mode: 'text',
      pythonOptions: ['-u'],
      scriptPath: scriptPath,
      args: [JSON.stringify(inputimage)]
    };

    const pyshell = new PythonShell('InitialModel.py', options);
    // Rest of your code
      pyshell.send('Hello, Python!');

          pyshell.on('message', message => {
            pythondata = message;
            myData.push(message);
            console.log(message);
          });

          pyshell.on('error', err => {
            console.error('Python error:', err);
          });

          pyshell.end((err, code, signal) => {
            if (err) {
              console.error('Python script execution failed:', err);
              res.status(500).send('Internal Server Error');
            } else {
              console.log('Python script execution completed with code', code);
              res.send({ shopifyData: shopifyapidata, pythonData: myData });
            }
          });
  
  }
});
        }
      }

      fetchNextPage();
    })
    .catch(function(error) {
      console.error(error);
      res.status(500).send('Internal Server Error');
    });
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Server running at port 3000");
});

