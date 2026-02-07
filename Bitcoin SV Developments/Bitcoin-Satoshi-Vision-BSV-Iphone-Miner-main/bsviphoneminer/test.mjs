import * as bsv from "bsv-wasm";
import crypto from "crypto";
import bs58check from "bs58check";

// Generate a random valid WIF string for BSV mainnet
function generateRandomWIF() {
  const privateKeyBytes = crypto.randomBytes(32);
  const version = Buffer.from([0x80]); // mainnet prefix
  const compressedFlag = Buffer.from([0x01]); // compressed key flag

  // Concatenate version + privkey + compressed flag
  const payload = Buffer.concat([version, privateKeyBytes, compressedFlag]);

  // Encode with base58check
  const wif = bs58check.encode(payload);
  return wif;
}

function validateOrGenerateKey(wif) {
  try {
    const privateKey = bsv.PrivateKey.fromWIF(wif);
    console.log("Private key is valid:", privateKey.toWIF());
    return privateKey;
  } catch (e) {
    console.warn("Invalid WIF provided:", e.message);
    console.log("Generating a new valid private key...");

    const newWIF = generateRandomWIF();
    const newPrivateKey = bsv.PrivateKey.fromWIF(newWIF);
    console.log("New valid private key generated:", newPrivateKey.toWIF());
    return newPrivateKey;
  }
}

const inputWIF = "L4mEiNgyBFDn6jMk9NxEG2q4tFv4zGaqxCgWqBEPzVCRj2wExqXp";
const privateKey = validateOrGenerateKey(inputWIF);
