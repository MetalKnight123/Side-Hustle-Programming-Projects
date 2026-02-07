// server.js
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const bsv = require('bsv-wasm');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

const privateKeyWIF = process.env.BSV_PRIVATE_KEY;

let privateKey;
try {
  privateKey = bsv.PrivateKey.fromWIF(privateKeyWIF);
  console.log('Private key loaded:', privateKey.toWIF());
} catch (err) {
  console.error('Failed to load private key:', err);
  process.exit(1); // exit if private key invalid
}

app.use(express.static('public'));
// Example send route stub (expand with actual transaction logic)
app.post('/send', (req, res) => {
  const { toAddress, amountSatoshis } = req.body;

  if (!toAddress || !amountSatoshis) {
    return res.status(400).json({ success: false, error: 'Missing parameters' });
  }

  // TODO: Build and broadcast transaction here using bsv-wasm and privateKey

  // For now, just simulate success response:
  return res.json({ success: true, txid: 'fake-txid-1234567890' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
