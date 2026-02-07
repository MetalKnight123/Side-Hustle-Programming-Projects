import os
import stripe
import time
import hashlib
import json
import uuid 
from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from decimal import Decimal, InvalidOperation
import json, os, time, hashlib
from flask import Flask, jsonify, request, session
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1
from flask import jsonify
from flask import Flask, request, jsonify, session
import traceback

# pip install flask mnemonic ecdsa
# pip install stripe


app = Flask(__name__)
app.secret_key = os.urandom(24)

mnemo = Mnemonic("english")

CREATED_WALLET = {}

#In this area of code the Mock quantum signer class is created. 
class MockQuantumSafeSigner:
    def __init__(self):
        self.session_private_key = os.urandom(32)
        self.session_public_key = hashlib.sha256(self.session_private_key).hexdigest()

    def generate_keypair(self):
        return self.session_public_key.encode()

    def export_secret_key(self):
        return self.session_private_key

def generate_keys():
    #In this block of code the ECDSA keys are generated. 
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    session_private_key = sk.to_string().hex()
    session_public_key = vk.to_string().hex()

    #This particular area of the code generates the mock quantum keys.
    signer = MockQuantumSafeSigner()
    session_quantum_public_key = signer.generate_keypair().decode()
    session_quantum_private_key = signer.export_secret_key().hex()

    #For this part of the code there is mnemonic and seed phrase which are developed.

    return session_public_key, session_private_key, session_quantum_public_key, session_quantum_private_key

#For this section, the Mock quantum signer class is created. 
class MockQuantumSafeSigner:
    def __init__(self):
        self.private_key = os.urandom(32)
        self.public_key = hashlib.sha256(self.private_key).hexdigest()

    def generate_keypair(self):
        return self.public_key.encode()

    def export_secret_key(self):
        return self.private_key

def generate_keys():
    #In this section of code the ECDSA keys are generated. 
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    #In this section of code the  mock quantum keys are generated. 
    signer = MockQuantumSafeSigner()
    quantum_public_key = signer.generate_keypair().decode()
    quantum_private_key = signer.export_secret_key().hex()

    #In this code section the mnemonic and seed phrase are generated. 
    seed_phrase = mnemo.generate(strength=128)

    return public_key, private_key, quantum_public_key, quantum_private_key, seed_phrase

#This part of the program fixes the email, password, balance. 
EMAIL = "trippy1121@icloud.com"
PASSWORD = "bellamaekittyissocute1121"
DEVELOPERBALANCE = 1050000
BALANCE = f"{DEVELOPERBALANCE}"
# This particular section generates the wallet keys once at the systems startup. 
public_key, private_key, quantum_public_key, quantum_private_key, seed_phrase = generate_keys()

CREATED_BALANCE = 0
NEWBALANCE = f"{CREATED_BALANCE} Pixelcoin (PXL)"

DEVELOPER_WALLET = {
    "email": EMAIL,
    "password": PASSWORD,
    "public_key": public_key,
    "quantum_public_key": quantum_public_key,
    "private_key": private_key,
    "quantum_private_key": quantum_private_key,
    "seed_phrase": seed_phrase,
    "balance": BALANCE
}

CREATED_WALLET = {
    "quantum_public_key": quantum_public_key,
    "balance": NEWBALANCE
}

WALLETS_FILE = "static/created_pixelcoin_blockchain_wallets.json"

def save_wallets_to_file():
    with open(WALLETS_FILE, "w") as f:
        json.dump(CREATED_WALLET, f, indent=4)

@app.route("/create_wallet", methods=["POST"])
def create_wallet_route():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    #This part of the program generates the ECDSA key pair.
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    #This block of code generates a quantum-safe key with the mock signer. 
    signer = MockQuantumSafeSigner()
    quantum_public_key = signer.generate_keypair().decode()
    quantum_private_key = signer.export_secret_key().hex()

    #This part of the code generates a seed phrase. 
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)

    #This part of the code displays an example balance for reference. 
    balance = 0

    #This part of the program allows storage in memory or for IndexedDB by assuming that the CREATED_WALLET dictionary exists.
    CREATED_WALLET[email] = {
        "email": email,
        "password": password,
        "public_create_key": public_key,
        "private_create_key": private_key,
        "quantum_create_public_key": quantum_public_key,
        "quantum_create_private_key": quantum_private_key,
        "seed_create_phrase": seed_phrase,
        "balance_created": balance
    }

    #This part of the program saves the data to the file after updating the wallet information.
    save_wallets_to_file()

    return jsonify(CREATED_WALLET[email])

@app.route('/developer_wallet', methods=['GET'])
def get_developer_wallet():
    return jsonify(DEVELOPER_WALLET)

@app.route('/created_wallet', methods=['GET'])
def get_created_wallet():
    return jsonify(CREATED_WALLET)

#This part of the program generates a wallet for a person that creates a wallet.
class CreateMockQuantumSafeSigner:
    def __init__(self):
        self.private_create_key = os.urandom(32)
        self.public_create_key = hashlib.sha256(self.private_create_key).hexdigest()

    def generatenew_keypair(self):
        return self.public_create_key.encode()

    def exportnew_secret_key(self):
        return self.private_create_key

def generatenew_keys():
    #This part of the program generates the ECDSA keys.
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    #This part of code is used to generate the mock signed quantum keys for security. 
    signer = CreateMockQuantumSafeSigner()
    quantum_create_public_key = signer.generatenew_keypair().decode()
    quantum_create_private_key = signer.exportnew_secret_key().hex()

    #This part of the program is used to generate a mnemonic seed phrase.
    seed_create_phrase = mnemo.generate(strength=128)

    return public_key, private_key, quantum_create_public_key, quantum_create_private_key, seed_create_phrase

user_wallets = {}  #This block of code uses a global dictionary to store wallets that are keyed by email.

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        data = request.get_json()
        email = data.get('email').strip()
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        #This part of the program loads existing wallets.
        wallets = {}
        if os.path.exists(WALLETS_FILE):
            with open(WALLETS_FILE, 'r') as f:
                wallets = json.load(f)

        #This part of the code only considers user wallets to skip session keys.
        user_wallets = {k: v for k, v in wallets.items() if k not in ["quantum_public_key", "balance"]}

        #This block section of code Checks if the email already exists.
        if email in user_wallets:
            return jsonify({"success": False, "message": "Wallet with this email already exists"}), 400

        #This part of the program generates wallet data as placeholder keys.
        wallet_data = {
            "email": email,
            "password": password,
            "public_create_key": "GENERATED_PUBLIC_KEY",
            "private_create_key": "GENERATED_PRIVATE_KEY",
            "quantum_create_public_key": "GENERATED_QUANTUM_PUBLIC_KEY",
            "quantum_create_private_key": "GENERATED_QUANTUM_PRIVATE_KEY",
            "seed_create_phrase": "GENERATED_SEED_PHRASE",
            "balance_created": 0
        }

        # This part of the program adds a new wallet and turns it into wallet data.
        wallets[email] = wallet_data

        #This part of the program ensures that session wallet keys exist.
        if "quantum_public_key" not in wallets:
            wallets["quantum_public_key"] = "SESSION_PUBLIC_KEY"
        if "balance" not in wallets:
            wallets["balance"] = "0 Pixelcoin (PXL)"

        #This part of the program saves back the wallets file. 
        with open(WALLETS_FILE, 'w') as f:
            json.dump(wallets, f, indent=4)

        return jsonify({"success": True, "wallet": wallet_data})

    except Exception as e:
        print("Error creating wallet:", e)
        return jsonify({"success": False, "message": str(e)}), 500


#This part of the program creates a python quantum mocksigner for public and private keys.
class MockQuantumSafeSigner:
    def __init__(self):
        self.private_key = os.urandom(32)
        self.public_key = hashlib.sha256(self.private_key).hexdigest()

    def generate_keypair(self):
        # Return public key bytes
        return self.public_key.encode()

    def export_secret_key(self):
        return self.private_key

    def import_secret_key(self, private_key_bytes):
        self.private_key = private_key_bytes
        self.public_key = hashlib.sha256(self.private_key).hexdigest()

    def sign(self, message: bytes):
        return hashlib.sha256(self.private_key + message).digest()

    def verify(self, message: bytes, signature: bytes, public_key_bytes: bytes):
        expected_pub = self.public_key.encode()
        if public_key_bytes != expected_pub:
            return False
        expected_sig = hashlib.sha256(self.private_key + message).digest()
        return signature == expected_sig

#This part of the program replaces oqs module and quantum algorithm with a mock signer.
oqs = None
QUANTUM_ALGO = "MockDilithium2"  #This part of the program is a placeholder to define the quantum algorithm.

mnemo = Mnemonic("english")  #This part of the program adds the mnemonic for mock signing.

def generate_quantum_wallet():
    signer = MockQuantumSafeSigner()
    public_key = signer.generate_keypair()
    private_key = signer.export_secret_key()
    seed_phrase = mnemo.generate(strength=128)

    return {
        "public_key": public_key.decode(),
        "private_key": private_key.hex(),
        "seed_phrase": seed_phrase,
        "balance": 0,
        "quantum_algorithm": QUANTUM_ALGO
    }

user_wallets = {}

#This part of the code is used to assign the developer wallet in the format below. 
user_wallets[DEVELOPER_WALLET["email"]] = DEVELOPER_WALLET

def sign_transaction_quantum(private_key_hex, message: str):
    signer = MockQuantumSafeSigner()
    signer.import_secret_key(bytes.fromhex(private_key_hex))
    signature = signer.sign(message.encode())
    return signature.hex()

def verify_transaction_quantum(public_key_str, message: str, signature_hex: str):
    signer = MockQuantumSafeSigner()
    #This part of the code uses public key bytes from a string (utf-8 encoded hex string).
    public_key_bytes = public_key_str.encode()
    signature = bytes.fromhex(signature_hex)
    return signer.verify(message.encode(), signature, public_key_bytes)

@app.route("/create_quantum_wallet", methods=["POST"])
def create_quantum_wallet():
    data = request.get_json()
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"})
    if email in user_wallets:
        return jsonify({"success": False, "message": "Email already registered"})

    quantum_wallet = generate_quantum_wallet()
    quantum_wallet["password"] = password
    user_wallets[email] = quantum_wallet
    session["email"] = email
    session["wallet"] = quantum_wallet
    return jsonify({
        "success": True,
        "message": "Quantum-safe wallet created (mock)",
        "public_key": quantum_wallet["public_key"]
    })
#This part of the program displays the Merge-Link Blockchain classes.-

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, validator):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.validator = validator
        self.hash = self.calculate_hash()
        self.history_proof = self.generate_history_proof()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.validator}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def generate_history_proof(self):
        return hashlib.sha256((self.hash + str(time.time())).encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "validator": self.validator,
            "hash": self.hash,
            "history_proof": self.history_proof
        }

class MergeLinkBlockchain:
    def __init__(self):
        self.chain = []
        self.validators = {}
        self.leases = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), [], "0", "genesis")
        self.chain.append(genesis_block)

    def stake(self, validator_address, amount):
        self.validators[validator_address] = self.validators.get(validator_address, 0) + amount

    def lease_stake(self, user_address, validator_address):
        if validator_address in self.validators:
            self.leases[user_address] = validator_address

    def select_validator(self):
        total_stake = sum(self.validators.values())
        if total_stake == 0:
            return "no-validator"
        pick = int.from_bytes(os.urandom(4), "big") % total_stake
        current = 0
        for validator, stake in self.validators.items():
            current += stake
            if current > pick:
                return validator
        return "no-validator"

    def add_block(self, transactions):
        validator = self.select_validator()
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), transactions, previous_block.hash, validator)
        self.chain.append(new_block)
        self.chain = self.merge_sort_chain(self.chain)

    def merge_sort_chain(self, blocks):
        if len(blocks) <= 1:
            return blocks
        mid = len(blocks) // 2
        left = self.merge_sort_chain(blocks[:mid])
        right = self.merge_sort_chain(blocks[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        while left and right:
            if left[0].hash < right[0].hash:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left or right)
        return result

    def to_dict(self):
        return [block.to_dict() for block in self.chain]

blockchain = MergeLinkBlockchain()

#This part of the code is the extended Pixelcoin Blockchain Layer including the wallets and supply features.

WALLET_FILE = "static/created_pixelcoin_blockchain_wallets.json"
MAX_SUPPLY = 21_000_000  #This part of the program sets the max supply to 21,000,000 Pixelcoins.

def load_wallets():
    with open(WALLET_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

def get_total_supply(wallets):
    total = 0
    for key, value in wallets.items():
        if isinstance(value, dict) and "balance_created" in value:
            total += int(value["balance_created"])
    return total

def get_balance(email):
    wallets = load_wallets()
    if email not in wallets:
        return 0
    return wallets[email]["balance_created"]

def send_pxl(sender_email, recipient_email, amount):
    wallets = load_wallets()

    if sender_email not in wallets:
        return {"success": False, "message": f"Sender wallet not found: {sender_email}"}
    if recipient_email not in wallets:
        return {"success": False, "message": f"Recipient wallet not found: {recipient_email}"}

    sender_balance = wallets[sender_email]["balance_created"]
    if sender_balance < amount:
        return {"success": False, "message": f"Insufficient balance! {sender_email} has {sender_balance} PXL."}

    #This part of the program deducts and credits balances. 
    wallets[sender_email]["balance_created"] -= amount
    wallets[recipient_email]["balance_created"] += amount
    save_wallets(wallets)

    #This section of the code controls the onchain transactions.
    transaction = {
        "from": sender_email,
        "to": recipient_email,
        "amount": float(amount),
        "timestamp": time.time()
    }
    blockchain.add_block([transaction])

    return {
        "success": True,
        "message": f"{sender_email} sent {amount} PXL to {recipient_email}.",
        "tx": transaction,
        "new_sender_balance": wallets[sender_email]["balance_created"],
        "new_recipient_balance": wallets[recipient_email]["balance_created"]
    }

def mint_pxl(to_email, amount):
    wallets = load_wallets()
    total_supply = get_total_supply(wallets)

    if total_supply + amount > MAX_SUPPLY:
        return {"success": False, "message": f"Cannot mint {amount} PXL. Supply limit (21M) reached."}

    if to_email not in wallets:
        return {"success": False, "message": f"Wallet not found for email: {to_email}"}

    wallets[to_email]["balance_created"] += amount
    save_wallets(wallets)

    tx = {
        "from": "SYSTEM",
        "to": to_email,
        "amount": amount,
        "timestamp": time.time(),
        "type": "mint"
    }
    blockchain.add_block([tx])

    return {"success": True, "message": f"Minted {amount} PXL to {to_email}", "tx": tx}

#This block of code developes the flask routes and session management to keep the program working.

@app.before_request
def ensure_wallet():
    #This part of the program only sets the developer wallet by default if no session wallet and not login or create routes were made.
    if 'wallet' not in session and request.endpoint not in ('login', 'create_wallet', 'static'):
        session['email'] = DEVELOPER_WALLET['email']
        session['wallet'] = DEVELOPER_WALLET

@app.route("/")
def home():
    developer_wallet = DEVELOPER_WALLET
    user_wallet = session.get('wallet')

    #This section of the code dsiplays other users public keys except the developers and the current users.
    other_public_keys = [w.get("public_key") for e,w in user_wallets.items()
                         if e not in (developer_wallet['email'], session.get('email'))]

    return render_template(
        "index.html",
        developer_wallet=developer_wallet,
        user_wallet=user_wallet,
        other_public_keys=other_public_keys
    )

@app.route("/developer")
def developer_keys():
    return jsonify(DEVELOPER_WALLET)

@app.route('/user_wallet')
def user_wallet():
    email = session.get("email")
    if not email:
        return jsonify({"error": "User not logged in"}), 401

    wallet = user_wallets.get(email)
    if not wallet:
        return jsonify({"error": "Wallet not found"}), 404

    return jsonify(wallet)


@app.route("/chain")
def get_chain():
    return jsonify(blockchain.to_dict())

@app.route("/stake", methods=["POST"])
def stake():
    data = request.get_json()
    validator = data.get("validator")
    amount = data.get("amount", 0)
    blockchain.stake(validator, amount)
    return jsonify({"message": f"Validator {validator} staked {amount} tokens."})

@app.route("/lease", methods=["POST"])
def lease():
    data = request.get_json()
    user = data.get("user")
    validator = data.get("validator")
    blockchain.lease_stake(user, validator)
    return jsonify({"message": f"User {user} leased stake to {validator}."})

@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.get_json()
    transactions = data.get("transactions", [])
    blockchain.add_block(transactions)
    return jsonify({"message": "Block added to blockchain."})

@app.route("/credit_tokens", methods=["POST"])
def credit_tokens():
    data = request.get_json()
    tokens = data.get("tokens", 0)
    wallet = session.get('wallet')
    if wallet:
        wallet['balance'] += tokens
        #This block of code is used to update the global variable for user_wallets so that you can store it.
        #This part of the program is used to try and update by email if the email exists so that there is a fallback through the public_key.
        email = session.get('email')
        if email in user_wallets:
            user_wallets[email]['balance'] = wallet['balance']
        else:
            #This part of the code is made as a fallback to find the wallet in user_wallets from the public_key.
            for w in user_wallets.values():
                if w.get('public_key') == wallet.get('public_key'):
                    w['balance'] = wallet['balance']
                    break
        session['wallet'] = wallet  #This part of the code is used to update the session.
        return jsonify({"message": f"Credited {tokens} PXL tokens to your wallet.", "new_balance": wallet['balance']})
    return jsonify({"error": "No wallet found"}), 404

#This part of the code is the newly created login and create wallet system. 

WALLETS_FILE = "static/created_pixelcoin_blockchain_wallets.json"

@app.route("/login", methods=["POST"])
def login():
    print("Login attempt received")

    #This section of code ensures that the wallet exists. 
    if not os.path.isfile(WALLETS_FILE):
        print("Wallets file not found:", WALLETS_FILE)
        return jsonify({"success": False, "message": "Wallets data file not found"}), 500

    #This part of the program loads the wallet data. 
    try:
        with open(WALLETS_FILE, "r") as f:
            user_wallets = json.load(f)
        print("Loaded wallets:", list(user_wallets.keys()))
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return jsonify({"success": False, "message": "Corrupted wallets data file"}), 500
    except Exception as e:
        print("General error loading wallets:", e)
        return jsonify({"success": False, "message": "Server error loading wallets"}), 500

    #This code block gets the credentials from the request upon logging in. 
    data = request.get_json()
    print("Received login data:", data)

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    #This part of the code looks up the wallet information.
    wallet = user_wallets.get(email)
    print(f"Looking for wallet for '{email}': {'Found' if wallet else 'Not found'}")

    #This part of the code checks the wallets credentials.
    if wallet and wallet.get("password") == password:
        session["email"] = email
        session["wallet"] = wallet
        print("Login successful for:", email)
        return jsonify({"success": True, "message": "Logged in successfully", "wallet": wallet})

    print("Login failed: invalid credentials")
    return jsonify({"success": False, "message": "Invalid email or password"}), 401


@app.route("/developer_wallet", methods=["POST"])
def create_developer_wallet():
    data = request.json or request.form
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"})

    if email in developer_wallets:
        return jsonify({"success": False, "message": "Email already registered"})

    new_wallet = generate_wallet()
    new_wallet["password"] = password
    developer_wallets[email] = new_wallet

    #This part of the code saves the developer wallets to the developer_wallets.json file.
    save_developer_wallets(developer_wallets)

    session["email"] = email
    session["wallet"] = new_wallet

    return jsonify({
        "success": True,
        "message": "Developer wallet created successfully",
        "public_key": new_wallet["public_key"]
    })

def save_developer_wallets(wallets):
    print("Saving developer wallets to developer_wallets.json...")
    with open("static/developer_wallet.json", "w") as f:
        json.dump(wallets, f, indent=4)
    print("Saved developer wallets.")

#This part of the code is optional by saving existing developer_wallets at the system startup (or remove it if that's unnecessary).
developer_wallets = DEVELOPER_WALLET
save_developer_wallets(developer_wallets)

def save_created_wallets(wallets):
    print("Saving developer wallets to developer_wallets.json...")
    with open("static/session_wallets.json", "w") as f:
        json.dump(wallets, f, indent=4)
    print("Saved developer wallets.")

created_wallets = CREATED_WALLET
save_created_wallets(created_wallets)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/wallet")
def serve_wallet_static():
    return app.send_static_file("wallet.html")

app = Flask(__name__)
app.secret_key = 'SwEbH/6db0RL2bXiSFpPrL7FXH4cV7vovSZoJENjVNW4QwkOlIOa9dcm+kGUIzTo'
#This part of the program is required to maintain the session management. 

DEVELOPER_WALLET = {
    "email": "trippy1121@icloud.com",
    "password": "bellamaekittyissocute1121",
    "public_key": "1HShkhAATBkdyreFVjfiasbHRvNijTqDJt",
    "private_key": "L2awQqW2pjQpHL92VxT6o4s6afswr8CgpSCdZ8cHBPQvHiDZGmdD",
    #This is the developer wallets sensitive information in this code block.
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email == DEVELOPER_WALLET['email'] and password == DEVELOPER_WALLET['password']:
        session['logged_in'] = True
        session['is_developer'] = True
        return jsonify({"success": True, "message": "Developer logged in"})
    else:
        #There could be added logic for everyday regular users in this section.
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})

@app.route('/developer_info')
def developer_info():
    if session.get('is_developer'):
        #This area of the code returns developer wallet information safely.
        return jsonify({
            "email": DEVELOPER_WALLET['email'],
            "public_key": DEVELOPER_WALLET['public_key'],
            "private_key": DEVELOPER_WALLET['private_key'],
            #This part of the program has additional information if needed. 
        })
    else:
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    #This block of code is the developer login information. 
    if email == DEVELOPER_WALLET.get('email') and password == DEVELOPER_WALLET.get('password'):
        session['logged_in'] = True
        session['is_developer'] = True
        return jsonify({"success": True})

    #This part of the program creates the wallet login feature.
    if 'CREATED_WALLET' in globals() and CREATED_WALLET.get('email') == email and CREATED_WALLET.get('password') == password:
        session['logged_in'] = True
        session['is_developer'] = False
        return jsonify({"success": True})

    #This part of the program returns invalid credentials.
    return jsonify({"success": False, "message": "Invalid credentials"}), 401


@app.route('/developer_info')
def developer_info():
    if session.get('is_developer'):
        return jsonify({
            "email": DEVELOPER_WALLET['email'],
            "public_key": DEVELOPER_WALLET['public_key'],
            "private_key": DEVELOPER_WALLET['private_key']
        })
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/session_wallet")
def session_wallet():
    if "wallet" not in session:
        #This part of the program creates a temorary wallet for the session.
        session["wallet"] = {
            "ecdsa_public_key": CREATED_WALLET['public_key'],
            "quantum_public_key": CREATED_WALLET['quantum_public_key'],
            "balance": 0,
            "label": "Temporary Session Wallet"
        }
    return jsonify(session["wallet"])

WALLET_FILE = 'static/created_pixelcoin_blockchain_wallets.json'

@app.route('/delete_wallet', methods=['POST'])
def delete_wallet():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        #This part of the program loads the JSON file path.
        if os.path.exists(WALLETS_FILE):
            with open(WALLETS_FILE, 'r') as f:
                wallets = json.load(f)
        else:
            wallets = {}

        #This part of the code checks if the key exists and whether it's a user wallet that skips the section keys.
        if email not in wallets:
            return jsonify({"success": False, "message": f"Wallet not found for email {email}"}), 404

        if email in ["quantum_public_key", "balance"]:
            return jsonify({"success": False, "message": "Cannot delete session keys"}), 400

        #This section of the code is specifically made to delete the users wallet. 
        del wallets[email]

        #This block section of code saves the wallet back to itself so it stores in the JSON file.
        with open(WALLETS_FILE, 'w') as f:
            json.dump(wallets, f, indent=4)

        return jsonify({"success": True})

    except Exception as e:
        print("Error deleting wallet:", e)
        return jsonify({"success": False, "message": str(e)}), 500



SESSION_WALLET = "static/session_wallets.json"

@app.route("/startup", methods=["POST"])
def startup():

    #This block of code is responsible for making sure that the file exists.
    if not os.path.isfile(SESSION_WALLET):
        print("Session wallet not found", SESSION_WALLET)
        return jsonify({"success": False, "message": "Session wallet data file not found"}), 500

    #This area of the code loads the wallet data.
    try:
        with open(SESSION_WALLET, "r") as f:
            user_wallets = json.load(f)
        print("Loaded wallets:", list(user_wallets.keys()))
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return jsonify({"success": False, "message": "Corrupted wallets data file"}), 500
    except Exception as e:
        print("General error loading wallets:", e)
        return jsonify({"success": False, "message": "Server error loading wallets"}), 500

    #This part of the program looks up the wallet to make sure its in the created wallets file.
    wallet = user_wallets.get(email)
    print(f"Looking for wallet for '{email}': {'Found' if wallet else 'Not found'}")

    # This section of code checks to make sure the credentials are valid. 
    if wallet and wallet.get("password") == password:
        session["email"] = email
        session["wallet"] = wallet
        print("Login successful for:", email)
        return jsonify({"success": True, "message": "Logged in successfully", "wallet": wallet})

    print("Login failed: invalid credentials")
    return jsonify({"success": False, "message": "Invalid email or password"}), 401

WALLET_FILE = 'static/created_pixelcoin_blockchain_wallets.json'

app = Flask(__name__)
WALLETS_FILE = os.path.join("static", "created_pixelcoin_blockchain_wallets.json")

def load_wallets():
    if not os.path.exists(WALLETS_FILE):
        return {}
    with open(WALLETS_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(WALLETS_FILE, "w") as f:
        json.dump(wallets, f, indent=2)

app = Flask(__name__)
app.secret_key = "super_secure_pixelcoin_key"
CORS(app)

WALLETS_FILE = "wallets.json"
BLOCKCHAIN_FILE = "blockchain.json"

#This section of code creates helper functions for the wallet paths.

def load_wallets():
    if os.path.exists(WALLETS_FILE):
        with open(WALLETS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_wallets(data):
    with open(WALLETS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def generate_txid(sender, recipient, amount):
    return hashlib.sha256(f"{sender}{recipient}{amount}{time.time()}".encode()).hexdigest()

#This block of code is used for creating new wallets.

@app.route("/create_wallet", methods=["POST"])
def create_wallet():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    wallets = load_wallets()
    if email in wallets:
        return jsonify({"success": False, "message": "Wallet already exists."}), 400

    #This block of code creates wallets with private and public keys. 
    private_key = hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    quantum_private_key = hashlib.sha256(f"QPRIV{private_key}".encode()).hexdigest()
    quantum_public_key = hashlib.sha256(quantum_private_key.encode()).hexdigest()
    seed_phrase = "pixelcoin " + str(uuid.uuid4())

    wallets[email] = {
        "email": email,
        "password": password,
        "public_key": public_key,
        "private_key": private_key,
        "quantum_public_key": quantum_public_key,
        "quantum_private_key": quantum_private_key,
        "seed_phrase": seed_phrase,
        "balance": "100.0"  #This is a placeholder where the wallets start out with 100 Pixelcoins.
    }

    save_wallets(wallets)

    return jsonify({
        "success": True,
        "email": email,
        "password": password,
        "public_key": public_key,
        "private_key": private_key,
        "quantum_public_key": quantum_public_key,
        "quantum_private_key": quantum_private_key,
        "seed_phrase": seed_phrase,
        "balance": "100.0"
    })

#This section of the code is the login and logout section for secure access to wallets.

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    wallets = load_wallets()  #This block of code allows all wallets to be loaded correctly.
    wallet = wallets.get(email)

    if not wallet or wallet.get("password") != password:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    session["user_email"] = email
    return jsonify({"success": True, "message": f"Logged in as {email}."})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_email", None)
    return jsonify({"success": True, "message": "Logged out successfully."})

#This part of the program allows Pixelcoin to be sent securely. 

def send_pixelcoin(sender_email, recipient_email, amount_str):
    try:
        amount = Decimal(amount_str)
    except (InvalidOperation, ValueError):
        return {"success": False, "message": "Invalid amount format."}

    if amount <= 0:
        return {"success": False, "message": "Amount must be positive."}

    wallets = load_wallets()

    if sender_email not in wallets:
        return {"success": False, "message": "Sender wallet not found."}
    if recipient_email not in wallets:
        return {"success": False, "message": "Recipient wallet not found."}

    sender_wallet = wallets[sender_email]
    recipient_wallet = wallets[recipient_email]

    sender_balance = Decimal(sender_wallet.get("balance", "0"))
    recipient_balance = Decimal(recipient_wallet.get("balance", "0"))

    if sender_balance < amount:
        return {"success": False, "message": "Insufficient Pixelcoin balance."}

    #For this block section of code, its purpose is to credit balances and deduct balances.
    sender_wallet["balance"] = str(sender_balance - amount)
    recipient_wallet["balance"] = str(recipient_balance + amount)

    #For this block of code, it is used to save wallets that have been updated. 
    wallets[sender_email] = sender_wallet
    wallets[recipient_email] = recipient_wallet
    save_wallets(wallets)

    #This part of the code is used to create a transaction record (history).
    tx = {
        "txid": generate_txid(sender_email, recipient_email, amount),
        "sender": sender_email,
        "recipient": recipient_email,
        "amount": str(amount),
        "timestamp": time.time()
    }

    # In this block of code the chain is appended to the blockchain to create successful transactions.
    chain = load_blockchain()
    chain.append(tx)
    save_blockchain(chain)

    return {"success": True, "tx": tx}

app = Flask(__name__)
app.secret_key = "pixelcoin-secret"  # This is the secret key that I made to allow the session for flask to continue.

def send_pxl(sender_email, recipient_email, amount):
    #I have not yet added the transaction logic here which means that it will return error.
    return f"Sent {amount} PXL from {sender_email} to {recipient_email}"

@app.route("/send_transaction", methods=["POST"])
def send_transaction():
    try:
        data = request.get_json(force=True)
        sender_email = session.get("user_email", "").strip().lower()
        recipient_email = data.get("recipient_email", "").strip().lower()
        amount = float(data.get("amount", 0))

        if not sender_email:
            return jsonify({"success": False, "message": "Not logged in."}), 401
        if not recipient_email or amount <= 0:
            return jsonify({"success": False, "message": "Recipient and positive amount required."}), 400

        result_message = send_pxl(sender_email, recipient_email, amount)
        return jsonify({"success": True, "message": result_message})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Server error: {e}"}), 500


#This was created as an optional login test to make sure the login section worked correctly.
@app.route("/login_test", methods=["POST"])
def login_test():
    """Set session email for testing"""
    data = request.get_json(force=True)
    session["user_email"] = data.get("email", "").strip().lower()
    return jsonify({"success": True, "message": f"Logged in as {session['user_email']}"})


#This particular block of code does a balance check to make sure that the balance is correct.

@app.route("/get_balance", methods=["POST"])
def get_balance():
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    wallets = load_wallets()
    wallet = wallets.get(email)

    if not wallet:
        return jsonify({"success": False, "message": "Wallet not found."}), 404

    balance = wallet.get("balance", "0")
    return jsonify({"success": True, "balance": balance})

#This area of the code allows the person using the frontend to view the transactions. 

@app.route("/transactions", methods=["GET"])
def transactions():
    chain = load_blockchain()
    return jsonify({"success": True, "transactions": chain})

#In this area of the code is where the delete wallet function is created. 

@app.route("/delete_wallet", methods=["POST"])
def delete_wallet():
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    wallets = load_wallets()
    if email not in wallets:
        return jsonify({"success": False, "message": "Wallet not found."}), 404

    del wallets[email]
    save_wallets(wallets)

    return jsonify({"success": True, "message": "Wallet deleted successfully."})

# In this aspect of the code, this is where the Server is being run from. 

@app.route("/get_wallet_info", methods=["POST"])
def get_wallet_info():
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    wallets = load_wallets()  #In this section, wallets are loaded from created_pixelcoin_blockchain_wallets.json.
    wallet = wallets.get(email)

    if not wallet:
        return jsonify({"success": False, "message": "Wallet not found."})

    return jsonify({
        "success": True,
        "email": wallet["email"],
        "password": wallet["password"],
        "public_key": wallet["public_key"],
        "private_key": wallet["private_key"],
        "quantum_public_key": wallet["quantum_public_key"],
        "quantum_private_key": wallet["quantum_private_key"],
        "seed_phrase": wallet["seed_phrase"],
        "balance": wallet["balance"]
    })

app = Flask(__name__)

# This is where the stripe api key is set to the api made for allowing payments.
stripe.api_key = "sk_test_51QeCn9Q03ruVESA4qOvQwpv9YgrMxaCcXm9ygZM72WlbPOZ3T1z77Db4yUr8uI8YbSUZ0JQKXoJ1XZwih8Ci0yDx00L8mujtQ9"

@app.route('/purchase_tokens', methods=['POST'])
def purchase_tokens():
    data = request.json
    email = data.get("email")
    token_amount = data.get("token_amount")  #This is the amount of Pixelcoins being charged.
    payment_method_id = data.get("payment_method_id")  #This is where the frontend retrieves the stripe payments.

    if not email or token_amount is None or not payment_method_id:
        return jsonify({"success": False, "message": "Missing data"}), 400

    try:
        #This part of the program charges the customer $1 a token.
        payment_intent = stripe.PaymentIntent.create(
            amount=int(token_amount * 100),  # Amount in cents
            currency='usd',
            payment_method=payment_method_id,
            confirm=True
        )

        # This part of the program loads the wallets from the JSON file.
        with open('static/created_pixelcoin_blockchain_wallets.json', 'r') as f:
            wallets = json.load(f)

        #This part of the program adds pixelcoins to the wallet. 
        if email not in wallets:
            return jsonify({"success": False, "message": "Wallet not found"}), 404

        wallets[email]['balance_created'] = wallets[email].get('balance_created', 0) + token_amount

        #This part of the program saves the wallet back into the JSON file. 
        with open('static/created_pixelcoin_blockchain_wallets.json', 'w') as f:
            json.dump(wallets, f, indent=4)

        return jsonify({"success": True, "message": f"Added {token_amount} Pixelcoins to {email}"})

    except stripe.error.CardError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/get_transactions", methods=["POST"])
def get_transactions():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    try:
        with open("static/created_pixelcoin_transactions.json", "r") as f:
            all_txns = json.load(f)
    except FileNotFoundError:
        all_txns = {}

    user_txns = all_txns.get(email, [])

    return jsonify({"success": True, "transactions": user_txns})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

WALLET_FILE = "static/created_pixelcoin_blockchain_wallets.json"

def load_wallets():
    with open(WALLET_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

@app.route("/send", methods=["POST"])
#In this section, send Pixelcoin gets the data with the amount of Pixelcoin from the Json.
def send_pxl():
    data = request.json
    recipient_email = data.get("email")
    amount = 10

    #This part of the program loads the wallets from the wallets section.
    wallets = load_wallets()

    #This part of the program converts the main_wallet_balance from an integer to a string.
    main_wallet_balance = int(wallets["balance"].split()[0])

    #This part of the program checks whether there is balance stored in the wallet.
    if main_wallet_balance < amount:
        return jsonify({"status": "error", "message": f"Insufficient balance! Main wallet has {main_wallet_balance} PXL."})

    #This part of the program checks to see if their is recipient email 
    #stored in the json file so it dosent send to a wallet not on the blockhain.
    if recipient_email not in wallets:
        return jsonify({"status": "error", "message": f"No wallet found for email: {recipient_email}"})

    #This part of the program gets the amount from the main_wallet_balance.
    wallets["balance"] = f"{main_wallet_balance - amount} Pixelcoin (PXL)"

    #This part of the program created the recipient email with the  amount of PXL to send.
    wallets[recipient_email]["balance_created"] += amount

    #This part of the program has wallets stored in the save_wallets function.
    save_wallets(wallets)
    
    #This part of the code adds the Pixelcoin balance and email stored into the Json File.
    return jsonify({
        "status": "success",
        "message": f"Successfully sent {amount} PXL to {recipient_email}.",
        "new_balance": wallets[recipient_email]["balance_created"],
        "main_wallet_balance": wallets["balance"]
    })

#This part of the program debugs the app when it starts up.
if __name__ == "__main__":
    app.run(debug=True)
