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

# Mock quantum signer class
class MockQuantumSafeSigner:
    def __init__(self):
        self.session_private_key = os.urandom(32)
        self.session_public_key = hashlib.sha256(self.session_private_key).hexdigest()

    def generate_keypair(self):
        return self.session_public_key.encode()

    def export_secret_key(self):
        return self.session_private_key

def generate_keys():
    # Generate ECDSA keys
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    session_private_key = sk.to_string().hex()
    session_public_key = vk.to_string().hex()

    # Generate mock quantum keys
    signer = MockQuantumSafeSigner()
    session_quantum_public_key = signer.generate_keypair().decode()
    session_quantum_private_key = signer.export_secret_key().hex()

    # Generate mnemonic seed phrase

    return session_public_key, session_private_key, session_quantum_public_key, session_quantum_private_key

# Mock quantum signer class
class MockQuantumSafeSigner:
    def __init__(self):
        self.private_key = os.urandom(32)
        self.public_key = hashlib.sha256(self.private_key).hexdigest()

    def generate_keypair(self):
        return self.public_key.encode()

    def export_secret_key(self):
        return self.private_key

def generate_keys():
    # Generate ECDSA keys
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    # Generate mock quantum keys
    signer = MockQuantumSafeSigner()
    quantum_public_key = signer.generate_keypair().decode()
    quantum_private_key = signer.export_secret_key().hex()

    # Generate mnemonic seed phrase
    seed_phrase = mnemo.generate(strength=128)

    return public_key, private_key, quantum_public_key, quantum_private_key, seed_phrase

# Fixed email, password, balance
EMAIL = "trippy1121@icloud.com"
PASSWORD = "bellamaekittyissocute1121"
DEVELOPERBALANCE = 1050000
BALANCE = f"{DEVELOPERBALANCE}"
# Generate wallet keys once at startup
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

    # Generate ECDSA key pair
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    # Generate quantum-safe key (using mock signer)
    signer = MockQuantumSafeSigner()
    quantum_public_key = signer.generate_keypair().decode()
    quantum_private_key = signer.export_secret_key().hex()

    # Generate seed phrase
    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)

    # Example balance
    balance = 0

    # Store in memory or DB (assuming CREATED_WALLET dict exists)
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

    # Save to file after update
    save_wallets_to_file()

    return jsonify(CREATED_WALLET[email])

@app.route('/developer_wallet', methods=['GET'])
def get_developer_wallet():
    return jsonify(DEVELOPER_WALLET)

@app.route('/created_wallet', methods=['GET'])
def get_created_wallet():
    return jsonify(CREATED_WALLET)

# Wallet generated for a person who creates a wallet.
class CreateMockQuantumSafeSigner:
    def __init__(self):
        self.private_create_key = os.urandom(32)
        self.public_create_key = hashlib.sha256(self.private_create_key).hexdigest()

    def generatenew_keypair(self):
        return self.public_create_key.encode()

    def exportnew_secret_key(self):
        return self.private_create_key

def generatenew_keys():
    # Generate ECDSA keys
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()

    # Generate mock quantum keys
    signer = CreateMockQuantumSafeSigner()
    quantum_create_public_key = signer.generatenew_keypair().decode()
    quantum_create_private_key = signer.exportnew_secret_key().hex()

    # Generate mnemonic seed phrase
    seed_create_phrase = mnemo.generate(strength=128)

    return public_key, private_key, quantum_create_public_key, quantum_create_private_key, seed_create_phrase

user_wallets = {}  # global dict to store wallets keyed by email

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        data = request.get_json()
        email = data.get('email').strip()
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        # Load existing wallets
        wallets = {}
        if os.path.exists(WALLETS_FILE):
            with open(WALLETS_FILE, 'r') as f:
                wallets = json.load(f)

        # Only consider user wallets (skip session keys)
        user_wallets = {k: v for k, v in wallets.items() if k not in ["quantum_public_key", "balance"]}

        # Check if email already exists
        if email in user_wallets:
            return jsonify({"success": False, "message": "Wallet with this email already exists"}), 400

        # Generate wallet data (placeholder keys)
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

        # Add new wallet
        wallets[email] = wallet_data

        # Ensure session keys exist
        if "quantum_public_key" not in wallets:
            wallets["quantum_public_key"] = "SESSION_PUBLIC_KEY"
        if "balance" not in wallets:
            wallets["balance"] = "0 Pixelcoin (PXL)"

        # Save back
        with open(WALLETS_FILE, 'w') as f:
            json.dump(wallets, f, indent=4)

        return jsonify({"success": True, "wallet": wallet_data})

    except Exception as e:
        print("Error creating wallet:", e)
        return jsonify({"success": False, "message": str(e)}), 500


# Simple pure Python mock quantum-safe signer
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

# Replace oqs module and quantum algorithm with mock signer
oqs = None
QUANTUM_ALGO = "MockDilithium2"  # Just a placeholder

mnemo = Mnemonic("english")  # assuming you have Mnemonic imported

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

# then you can assign the developer wallet like this:
user_wallets[DEVELOPER_WALLET["email"]] = DEVELOPER_WALLET

def sign_transaction_quantum(private_key_hex, message: str):
    signer = MockQuantumSafeSigner()
    signer.import_secret_key(bytes.fromhex(private_key_hex))
    signature = signer.sign(message.encode())
    return signature.hex()

def verify_transaction_quantum(public_key_str, message: str, signature_hex: str):
    signer = MockQuantumSafeSigner()
    # Public key bytes from string (utf-8 encoded hex string)
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
# --- Merge-Link Blockchain classes ---

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

# --- Flask routes and session management ---

@app.before_request
def ensure_wallet():
    # Only set developer wallet by default if no session wallet AND not login or create routes
    if 'wallet' not in session and request.endpoint not in ('login', 'create_wallet', 'static'):
        session['email'] = DEVELOPER_WALLET['email']
        session['wallet'] = DEVELOPER_WALLET

@app.route("/")
def home():
    developer_wallet = DEVELOPER_WALLET
    user_wallet = session.get('wallet')

    # Show other users' public keys except developer and current user
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
        # Update global user_wallets store as well
        # Try to update by email if exists; fallback by public_key
        email = session.get('email')
        if email in user_wallets:
            user_wallets[email]['balance'] = wallet['balance']
        else:
            # fallback: find wallet in user_wallets by public_key
            for w in user_wallets.values():
                if w.get('public_key') == wallet.get('public_key'):
                    w['balance'] = wallet['balance']
                    break
        session['wallet'] = wallet  # Update session
        return jsonify({"message": f"Credited {tokens} PXL tokens to your wallet.", "new_balance": wallet['balance']})
    return jsonify({"error": "No wallet found"}), 404

# ========== NEW ADDED LOGIN/CREATE WALLET SYSTEM ==========


WALLETS_FILE = "static/created_pixelcoin_blockchain_wallets.json"

@app.route("/login", methods=["POST"])
def login():
    print("🔐 Login attempt received")

    # Ensure file exists
    if not os.path.isfile(WALLETS_FILE):
        print("❌ Wallets file not found:", WALLETS_FILE)
        return jsonify({"success": False, "message": "Wallets data file not found"}), 500

    # Load wallet data
    try:
        with open(WALLETS_FILE, "r") as f:
            user_wallets = json.load(f)
        print("📁 Loaded wallets:", list(user_wallets.keys()))
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return jsonify({"success": False, "message": "Corrupted wallets data file"}), 500
    except Exception as e:
        print("❌ General error loading wallets:", e)
        return jsonify({"success": False, "message": "Server error loading wallets"}), 500

    # Get credentials from request
    data = request.get_json()
    print("📨 Received login data:", data)

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400

    # Look up wallet
    wallet = user_wallets.get(email)
    print(f"🔍 Looking for wallet for '{email}': {'Found' if wallet else 'Not found'}")

    # Check credentials
    if wallet and wallet.get("password") == password:
        session["email"] = email
        session["wallet"] = wallet
        print("✅ Login successful for:", email)
        return jsonify({"success": True, "message": "Logged in successfully", "wallet": wallet})

    print("❌ Login failed: invalid credentials")
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

    # ✅ Save developer wallets to developer_wallets.json
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

# Optional: Save existing developer_wallets at startup (or remove if unnecessary)
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
app.secret_key = 'SwEbH/6db0RL2bXiSFpPrL7FXH4cV7vovSZoJENjVNW4QwkOlIOa9dcm+kGUIzTo'  # Required for session management

DEVELOPER_WALLET = {
    "email": "trippy1121@icloud.com",
    "password": "bellamaekittyissocute1121",
    "public_key": "1HShkhAATBkdyreFVjfiasbHRvNijTqDJt",
    "private_key": "L2awQqW2pjQpHL92VxT6o4s6afswr8CgpSCdZ8cHBPQvHiDZGmdD",
    # other sensitive info...
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
        # Could add logic for regular users here
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})

@app.route('/developer_info')
def developer_info():
    if session.get('is_developer'):
        # Return developer wallet info safely
        return jsonify({
            "email": DEVELOPER_WALLET['email'],
            "public_key": DEVELOPER_WALLET['public_key'],
            "private_key": DEVELOPER_WALLET['private_key'],
            # Other info if needed
        })
    else:
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Developer login
    if email == DEVELOPER_WALLET.get('email') and password == DEVELOPER_WALLET.get('password'):
        session['logged_in'] = True
        session['is_developer'] = True
        return jsonify({"success": True})

    # Created wallet login
    if 'CREATED_WALLET' in globals() and CREATED_WALLET.get('email') == email and CREATED_WALLET.get('password') == password:
        session['logged_in'] = True
        session['is_developer'] = False
        return jsonify({"success": True})

    # Invalid credentials
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
        # Create temporary wallet
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

        # Load JSON
        if os.path.exists(WALLETS_FILE):
            with open(WALLETS_FILE, 'r') as f:
                wallets = json.load(f)
        else:
            wallets = {}

        # Check if key exists and is a user wallet (skip session keys)
        if email not in wallets:
            return jsonify({"success": False, "message": f"Wallet not found for email {email}"}), 404

        if email in ["quantum_public_key", "balance"]:
            return jsonify({"success": False, "message": "Cannot delete session keys"}), 400

        # Delete the user wallet
        del wallets[email]

        # Save back
        with open(WALLETS_FILE, 'w') as f:
            json.dump(wallets, f, indent=4)

        return jsonify({"success": True})

    except Exception as e:
        print("Error deleting wallet:", e)
        return jsonify({"success": False, "message": str(e)}), 500



SESSION_WALLET = "static/session_wallets.json"

@app.route("/startup", methods=["POST"])
def startup():

    # Ensure file exists
    if not os.path.isfile(SESSION_WALLET):
        print("Session wallet not found", SESSION_WALLET)
        return jsonify({"success": False, "message": "Session wallet data file not found"}), 500

    # Load wallet data
    try:
        with open(SESSION_WALLET, "r") as f:
            user_wallets = json.load(f)
        print("📁 Loaded wallets:", list(user_wallets.keys()))
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return jsonify({"success": False, "message": "Corrupted wallets data file"}), 500
    except Exception as e:
        print("❌ General error loading wallets:", e)
        return jsonify({"success": False, "message": "Server error loading wallets"}), 500

    # Look up wallet
    wallet = user_wallets.get(email)
    print(f"🔍 Looking for wallet for '{email}': {'Found' if wallet else 'Not found'}")

    # Check credentials
    if wallet and wallet.get("password") == password:
        session["email"] = email
        session["wallet"] = wallet
        print("✅ Login successful for:", email)
        return jsonify({"success": True, "message": "Logged in successfully", "wallet": wallet})

    print("❌ Login failed: invalid credentials")
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

# ==========================
# Helper Functions
# ==========================

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

# ==========================
# Wallet Creation
# ==========================

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

    # Simulate wallet creation (public/private keys)
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
        "balance": "100.0"  # Start with 100 Pixelcoins
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

# ==========================
# Login / Logout
# ==========================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    wallets = load_wallets()  # load all wallets
    wallet = wallets.get(email)

    if not wallet or wallet.get("password") != password:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    session["user_email"] = email
    return jsonify({"success": True, "message": f"Logged in as {email}."})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_email", None)
    return jsonify({"success": True, "message": "Logged out successfully."})

# ==========================
# Send Pixelcoin (Secure)
# ==========================

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

    # Deduct and credit balances
    sender_wallet["balance"] = str(sender_balance - amount)
    recipient_wallet["balance"] = str(recipient_balance + amount)

    # Save updated wallets
    wallets[sender_email] = sender_wallet
    wallets[recipient_email] = recipient_wallet
    save_wallets(wallets)

    # Create transaction record
    tx = {
        "txid": generate_txid(sender_email, recipient_email, amount),
        "sender": sender_email,
        "recipient": recipient_email,
        "amount": str(amount),
        "timestamp": time.time()
    }

    # Append to blockchain
    chain = load_blockchain()
    chain.append(tx)
    save_blockchain(chain)

    return {"success": True, "tx": tx}

@app.route("/send_transaction", methods=["POST"])
def send_transaction():
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    sender_email = session["user_email"]
    recipient_email = data.get("recipient_email", "").strip().lower()
    amount = data.get("amount")

    result = send_pixelcoin(sender_email, recipient_email, str(amount))
    return jsonify(result)

# ==========================
# Balance Check
# ==========================

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

# ==========================
# View All Transactions
# ==========================

@app.route("/transactions", methods=["GET"])
def transactions():
    chain = load_blockchain()
    return jsonify({"success": True, "transactions": chain})

# ==========================
# Delete Wallet
# ==========================

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

# ==========================
# Run Server
# ==========================


@app.route("/get_wallet_info", methods=["POST"])
def get_wallet_info():
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    wallets = load_wallets()  # loads from created_pixelcoin_blockchain_wallets.json
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

# Replace with your Stripe secret key
stripe.api_key = "sk_test_51QeCn9Q03ruVESA4qOvQwpv9YgrMxaCcXm9ygZM72WlbPOZ3T1z77Db4yUr8uI8YbSUZ0JQKXoJ1XZwih8Ci0yDx00L8mujtQ9"

@app.route('/purchase_tokens', methods=['POST'])
def purchase_tokens():
    data = request.json
    email = data.get("email")
    token_amount = data.get("token_amount")  # How many Pixelcoins to credit
    payment_method_id = data.get("payment_method_id")  # Stripe PaymentMethod ID from frontend

    if not email or token_amount is None or not payment_method_id:
        return jsonify({"success": False, "message": "Missing data"}), 400

    try:
        # Charge the customer (example: $1 per token)
        payment_intent = stripe.PaymentIntent.create(
            amount=int(token_amount * 100),  # Amount in cents
            currency='usd',
            payment_method=payment_method_id,
            confirm=True
        )

        # Load wallets JSON
        with open('static/created_pixelcoin_blockchain_wallets.json', 'r') as f:
            wallets = json.load(f)

        # Add tokens to wallet
        if email not in wallets:
            return jsonify({"success": False, "message": "Wallet not found"}), 404

        wallets[email]['balance_created'] = wallets[email].get('balance_created', 0) + token_amount

        # Save back to JSON
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