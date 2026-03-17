# # import os
# # from flask import Flask, request, jsonify, render_template
# # from flask_cors import CORS
# # from groq import Groq
# # from dotenv import load_dotenv
# # import logging

# # # Load environment variables from .env file
# # load_dotenv()

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # Initialize Flask app
# # app = Flask(__name__)
# # CORS(app)

# # # Get API key from environment
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # # Initialize Groq client
# # client = None
# # if GROQ_API_KEY:
# #     try:
# #         client = Groq(api_key=GROQ_API_KEY)
# #         logger.info("✓ Groq client initialized successfully")
# #     except Exception as e:
# #         logger.error(f"✗ Failed to initialize Groq client: {e}")
# # else:
# #     logger.error("✗ GROQ_API_KEY environment variable not set")

# # @app.route("/")
# # def home():
# #     """Serve the home page with the 3D chat interface"""
# #     return render_template("index.html")

# # @app.route("/chat", methods=["POST"])
# # def chat():
# #     """Handle chat requests"""
# #     try:
# #         if not client:
# #             return jsonify({"error": "API key not configured"}), 500

# #         # Get message from request
# #         data = request.get_json()
        
# #         if not data:
# #             return jsonify({"error": "No data provided"}), 400
        
# #         message = data.get("message", "").strip()
        
# #         if not message:
# #             return jsonify({"error": "Message is required"}), 400
        
# #         logger.info(f"Processing message: {message[:50]}...")
        
# #         # System prompt to make the AI respond like Claude
# #         system_prompt = """You are MAHADEV AI, an AI assistant made by Co-Member of Mahadev Group. You are helpful, harmless, and honest.

# # You should:
# # - Be thoughtful and clear in your responses
# # - Provide detailed, well-reasoned answers
# # - Use markdown formatting for better readability (bold, lists, code blocks when appropriate)
# # - Be concise but thorough
# # - Admit when you're uncertain about something
# # - Break down complex topics into understandable parts
# # - Use examples when helpful
# # - Be friendly and conversational

# # Format your responses with clear structure using markdown when appropriate."""
        
# #         # Call Groq API
# #         response = client.chat.completions.create(
# #             model="llama-3.3-70b-versatile",
# #             messages=[
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": message}
# #             ],
# #             max_tokens=1024,
# #             temperature=0.7
# #         )

# #         answer = response.choices[0].message.content
        
# #         return jsonify({"response": answer}), 200

# #     except Exception as e:
# #         logger.error(f"Error in chat endpoint: {str(e)}")
# #         return jsonify({"error": "Failed to process request"}), 500

# # @app.route("/api/health", methods=["GET"])
# # def health():
# #     """Health check endpoint"""
# #     return jsonify({
# #         "status": "healthy",
# #         "api_configured": bool(GROQ_API_KEY),
# #         "client_initialized": client is not None
# #     }), 200

# # if __name__ == "__main__":
# #     if not GROQ_API_KEY:
# #         print("\n" + "="*60)
# #         print("⚠️  WARNING: GROQ_API_KEY is not configured!")
# #         print("="*60)
# #         print("\nThe chatbot will not work without it.")
# #         print("\nPlease set your API key:")
# #         print("  1. Create a .env file in project root")
# #         print("  2. Add: GROQ_API_KEY=gsk_your_key_here")
# #         print("  3. Get your key from: https://console.groq.com/")
# #         print("\n" + "="*60 + "\n")
    
# #     app.run(debug=True, host="0.0.0.0", port=5000)


# import os
# import hashlib
# import secrets
# from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
# from flask_cors import CORS
# from groq import Groq
# from dotenv import load_dotenv
# import logging
# import mysql.connector
# from mysql.connector import Error
# from functools import wraps

# # Load environment variables from .env file
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
# CORS(app)

# # Get API key from environment
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # MySQL Configuration — set these in your .env file
# DB_CONFIG = {
#     "host":     os.getenv("MYSQL_HOST",     "localhost"),
#     "port":     int(os.getenv("MYSQL_PORT", "3306")),
#     "user":     os.getenv("MYSQL_USER",     "root"),
#     "password": os.getenv("MYSQL_PASSWORD", ""),
#     "database": os.getenv("MYSQL_DATABASE", "mahadev_ai"),
# }

# # Initialize Groq client
# client = None
# if GROQ_API_KEY:
#     try:
#         client = Groq(api_key=GROQ_API_KEY)
#         logger.info("✓ Groq client initialized successfully")
#     except Exception as e:
#         logger.error(f"✗ Failed to initialize Groq client: {e}")
# else:
#     logger.error("✗ GROQ_API_KEY environment variable not set")


# # ─────────────────────────────────────────────
# # DATABASE HELPERS
# # ─────────────────────────────────────────────

# def get_db():
#     """Return a new MySQL connection."""
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         return conn
#     except Error as e:
#         logger.error(f"MySQL connection error: {e}")
#         return None


# def init_db():
#     """Create the users table if it doesn't exist."""
#     # Connect without specifying the database first
#     tmp_config = {k: v for k, v in DB_CONFIG.items() if k != "database"}
#     try:
#         conn = mysql.connector.connect(**tmp_config)
#         cursor = conn.cursor()
#         cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
#         cursor.execute(f"USE `{DB_CONFIG['database']}`")
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id            INT AUTO_INCREMENT PRIMARY KEY,
#                 first_name    VARCHAR(80)  NOT NULL,
#                 last_name     VARCHAR(80)  NOT NULL,
#                 username      VARCHAR(80)  NOT NULL UNIQUE,
#                 email         VARCHAR(180) NOT NULL UNIQUE,
#                 password_hash VARCHAR(128) NOT NULL,
#                 created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         conn.commit()
#         logger.info("✓ Database and users table ready")
#     except Error as e:
#         logger.error(f"Database init error: {e}")
#     finally:
#         try:
#             cursor.close()
#             conn.close()
#         except Exception:
#             pass


# def hash_password(password: str) -> str:
#     salt = secrets.token_hex(16)
#     hashed = hashlib.sha256((salt + password).encode()).hexdigest()
#     return f"{salt}:{hashed}"


# def verify_password(password: str, stored: str) -> bool:
#     try:
#         salt, hashed = stored.split(":", 1)
#         return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
#     except ValueError:
#         return False


# def get_user_by_email(email: str):
#     conn = get_db()
#     if not conn:
#         return None
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         return cursor.fetchone()
#     except Error as e:
#         logger.error(f"DB error: {e}")
#         return None
#     finally:
#         cursor.close()
#         conn.close()


# def create_user(first_name, last_name, username, email, password):
#     conn = get_db()
#     if not conn:
#         return False, "Database connection failed"
#     try:
#         cursor = conn.cursor()
#         pw_hash = hash_password(password)
#         cursor.execute(
#             "INSERT INTO users (first_name, last_name, username, email, password_hash) VALUES (%s, %s, %s, %s, %s)",
#             (first_name, last_name, username, email, pw_hash)
#         )
#         conn.commit()
#         return True, "Account created successfully"
#     except mysql.connector.IntegrityError as e:
#         if "username" in str(e):
#             return False, "Username already taken"
#         elif "email" in str(e):
#             return False, "Email is already registered"
#         return False, "Registration failed"
#     except Error as e:
#         logger.error(f"Create user error: {e}")
#         return False, "Registration failed"
#     finally:
#         cursor.close()
#         conn.close()


# # ─────────────────────────────────────────────
# # AUTH DECORATOR
# # ─────────────────────────────────────────────

# def login_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect(url_for("login"))
#         return f(*args, **kwargs)
#     return decorated


# # ─────────────────────────────────────────────
# # ROUTES — AUTH
# # ─────────────────────────────────────────────

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if "user_id" in session:
#         return redirect(url_for("home"))

#     if request.method == "POST":
#         email    = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "")

#         if not email or not password:
#             flash("Email and password are required.", "error")
#             return render_template("login.html")

#         user = get_user_by_email(email)
#         if user and verify_password(password, user["password_hash"]):
#             session["user_id"]   = user["id"]
#             session["username"]  = user["username"]
#             session["full_name"] = f"{user['first_name']} {user['last_name']}"
#             logger.info(f"User logged in: {user['email']}")
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid email or password.", "error")

#     return render_template("login.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if "user_id" in session:
#         return redirect(url_for("home"))

#     if request.method == "POST":
#         first_name       = request.form.get("first_name", "").strip()
#         last_name        = request.form.get("last_name", "").strip()
#         username         = request.form.get("username", "").strip().lower()
#         email            = request.form.get("email", "").strip().lower()
#         password         = request.form.get("password", "")
#         confirm_password = request.form.get("confirm_password", "")

#         if not all([first_name, last_name, username, email, password]):
#             flash("All fields are required.", "error")
#             return render_template("register.html")

#         if len(password) < 6:
#             flash("Password must be at least 6 characters.", "error")
#             return render_template("register.html")

#         if password != confirm_password:
#             flash("Passwords do not match.", "error")
#             return render_template("register.html")

#         if len(username) < 3:
#             flash("Username must be at least 3 characters.", "error")
#             return render_template("register.html")

#         success, message = create_user(first_name, last_name, username, email, password)
#         if success:
#             flash("Account created! Please sign in.", "success")
#             return redirect(url_for("login"))
#         else:
#             flash(message, "error")

#     return render_template("register.html")


# @app.route("/logout")
# def logout():
#     username = session.get("username", "unknown")
#     session.clear()
#     logger.info(f"User logged out: {username}")
#     flash("You have been signed out.", "success")
#     return redirect(url_for("login"))


# # ─────────────────────────────────────────────
# # ROUTES — APP
# # ─────────────────────────────────────────────

# @app.route("/")
# @login_required
# def home():
#     """Serve the home page with the 3D chat interface"""
#     return render_template("index.html")


# @app.route("/chat", methods=["POST"])
# @login_required
# def chat():
#     """Handle chat requests"""
#     try:
#         if not client:
#             return jsonify({"error": "API key not configured"}), 500

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No data provided"}), 400

#         message = data.get("message", "").strip()
#         if not message:
#             return jsonify({"error": "Message is required"}), 400

#         logger.info(f"[{session.get('username')}] Processing: {message[:50]}...")

#         system_prompt = """You are MAHADEV AI, an AI assistant made by Co-Member of Mahadev Group. You are helpful, harmless, and honest.

# You should:
# - Be thoughtful and clear in your responses
# - Provide detailed, well-reasoned answers
# - Use markdown formatting for better readability (bold, lists, code blocks when appropriate)
# - Be concise but thorough
# - Admit when you're uncertain about something
# - Break down complex topics into understandable parts
# - Use examples when helpful
# - Be friendly and conversational

# Format your responses with clear structure using markdown when appropriate."""

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": message}
#             ],
#             max_tokens=1024,
#             temperature=0.7
#         )

#         answer = response.choices[0].message.content
#         return jsonify({"response": answer}), 200

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {str(e)}")
#         return jsonify({"error": "Failed to process request"}), 500


# @app.route("/api/health", methods=["GET"])
# def health():
#     """Health check endpoint"""
#     return jsonify({
#         "status": "healthy",
#         "api_configured": bool(GROQ_API_KEY),
#         "client_initialized": client is not None,
#         "logged_in": "user_id" in session,
#     }), 200


# # ─────────────────────────────────────────────
# # STARTUP
# # ─────────────────────────────────────────────

# if __name__ == "__main__":
#     if not GROQ_API_KEY:
#         print("\n" + "="*60)
#         print("⚠️  WARNING: GROQ_API_KEY is not configured!")
#         print("="*60)
#         print("\nThe chatbot will not work without it.")
#         print("\nPlease set your API key:")
#         print("  1. Create a .env file in project root")
#         print("  2. Add: GROQ_API_KEY=gsk_your_key_here")
#         print("  3. Get your key from: https://console.groq.com/")
#         print("\n" + "="*60 + "\n")

#     # Initialize database tables on startup
#     init_db()

#     app.run(debug=True, host="0.0.0.0", port=5000)


import os
import hashlib
import secrets
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import logging
import mysql.connector
from mysql.connector import Error
from functools import wraps

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST",     "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "user":     os.getenv("MYSQL_USER",     "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "mahadev_ai"),
}

client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        logger.info("✓ Groq client initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Groq client: {e}")
else:
    logger.error("✗ GROQ_API_KEY not set")


# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        logger.error(f"MySQL connection error: {e}")
        return None


def init_db():
    tmp = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    try:
        conn = mysql.connector.connect(**tmp)
        cur  = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
        cur.execute(f"USE `{DB_CONFIG['database']}`")

        # users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                first_name    VARCHAR(80)  NOT NULL,
                last_name     VARCHAR(80)  NOT NULL,
                username      VARCHAR(80)  NOT NULL UNIQUE,
                email         VARCHAR(180) NOT NULL UNIQUE,
                password_hash VARCHAR(128) NOT NULL,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # chat_sessions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                user_id    INT          NOT NULL,
                title      VARCHAR(255) NOT NULL DEFAULT 'New conversation',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                KEY idx_user (user_id),
                CONSTRAINT fk_cs_user FOREIGN KEY (user_id)
                    REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        """)

        # chat_messages
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                session_id INT  NOT NULL,
                user_id    INT  NOT NULL,
                role       ENUM('user','assistant') NOT NULL,
                content    TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                KEY idx_session (session_id),
                KEY idx_msg_user (user_id),
                CONSTRAINT fk_cm_session FOREIGN KEY (session_id)
                    REFERENCES chat_sessions(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT fk_cm_user FOREIGN KEY (user_id)
                    REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
            )
        """)

        conn.commit()
        logger.info("✓ All tables ready (users, chat_sessions, chat_messages)")
    except Error as e:
        logger.error(f"init_db error: {e}")
    finally:
        try: cur.close(); conn.close()
        except: pass


# ── password helpers ──────────────────────────

def hash_password(pw: str) -> str:
    salt = secrets.token_hex(16)
    return f"{salt}:{hashlib.sha256((salt+pw).encode()).hexdigest()}"

def verify_password(pw: str, stored: str) -> bool:
    try:
        salt, h = stored.split(":", 1)
        return hashlib.sha256((salt+pw).encode()).hexdigest() == h
    except ValueError:
        return False


# ── user helpers ──────────────────────────────

def get_user_by_email(email):
    conn = get_db()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        return cur.fetchone()
    except Error as e:
        logger.error(e); return None
    finally: cur.close(); conn.close()

def create_user(first_name, last_name, username, email, password):
    conn = get_db()
    if not conn: return False, "Database connection failed"
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (first_name,last_name,username,email,password_hash) VALUES (%s,%s,%s,%s,%s)",
            (first_name, last_name, username, email, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully"
    except mysql.connector.IntegrityError as e:
        if "username" in str(e): return False, "Username already taken"
        if "email"    in str(e): return False, "Email already registered"
        return False, "Registration failed"
    except Error as e:
        logger.error(e); return False, "Registration failed"
    finally: cur.close(); conn.close()


# ── chat session helpers ──────────────────────

def create_chat_session(user_id: int, title: str) -> int | None:
    """Insert a new chat_session row and return its id."""
    conn = get_db()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_sessions (user_id, title) VALUES (%s, %s)",
            (user_id, title[:255])
        )
        conn.commit()
        session_id = cur.lastrowid
        logger.info(f"Created chat_session id={session_id} for user_id={user_id}")
        return session_id
    except Error as e:
        logger.error(f"create_chat_session: {e}"); return None
    finally: cur.close(); conn.close()

def update_session_title(session_id: int, title: str):
    """Update the title of a chat session."""
    conn = get_db()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE chat_sessions SET title=%s WHERE id=%s",
            (title[:255], session_id)
        )
        conn.commit()
    except Error as e:
        logger.error(f"update_session_title: {e}")
    finally: cur.close(); conn.close()

def save_message(session_id: int, user_id: int, role: str, content: str):
    """Insert one message into chat_messages."""
    conn = get_db()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_messages (session_id, user_id, role, content) VALUES (%s,%s,%s,%s)",
            (session_id, user_id, role, content)
        )
        conn.commit()
        logger.info(f"Saved message role={role} session_id={session_id}")
    except Error as e:
        logger.error(f"save_message: {e}")
    finally: cur.close(); conn.close()

def get_session_messages(session_id: int):
    """Return all messages for a session ordered by created_at."""
    conn = get_db()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT role, content FROM chat_messages WHERE session_id=%s ORDER BY created_at ASC",
            (session_id,)
        )
        return cur.fetchall()
    except Error as e:
        logger.error(f"get_session_messages: {e}"); return []
    finally: cur.close(); conn.close()

def get_user_sessions(user_id: int):
    """Return all chat sessions for a user (newest first)."""
    conn = get_db()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, title, created_at FROM chat_sessions WHERE user_id=%s ORDER BY updated_at DESC",
            (user_id,)
        )
        return cur.fetchall()
    except Error as e:
        logger.error(f"get_user_sessions: {e}"); return []
    finally: cur.close(); conn.close()


# ─────────────────────────────────────────────
# AUTH DECORATOR
# ─────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")
        user = get_user_by_email(email)
        if user and verify_password(password, user["password_hash"]):
            session["user_id"]   = user["id"]
            session["username"]  = user["username"]
            session["full_name"] = f"{user['first_name']} {user['last_name']}"
            logger.info(f"Login: {user['email']}")
            return redirect(url_for("home"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        first_name       = request.form.get("first_name", "").strip()
        last_name        = request.form.get("last_name",  "").strip()
        username         = request.form.get("username",   "").strip().lower()
        email            = request.form.get("email",      "").strip().lower()
        password         = request.form.get("password",   "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([first_name, last_name, username, email, password]):
            flash("All fields are required.", "error")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return render_template("register.html")

        ok, msg = create_user(first_name, last_name, username, email, password)
        if ok:
            flash("Account created! Please sign in.", "success")
            return redirect(url_for("login"))
        flash(msg, "error")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
# APP ROUTES
# ─────────────────────────────────────────────

@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/api/sessions", methods=["GET"])
@login_required
def api_sessions():
    """Return all chat sessions for the logged-in user."""
    sessions = get_user_sessions(session["user_id"])
    # convert datetime to string for JSON
    for s in sessions:
        if s.get("created_at"):
            s["created_at"] = str(s["created_at"])
    return jsonify(sessions), 200


@app.route("/api/sessions/<int:session_id>/messages", methods=["GET"])
@login_required
def api_session_messages(session_id):
    """Return all messages for a specific session."""
    messages = get_session_messages(session_id)
    return jsonify(messages), 200


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    try:
        if not client:
            return jsonify({"error": "API key not configured"}), 500

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        message    = data.get("message", "").strip()
        session_id = data.get("session_id")   # may be None for first message

        if not message:
            return jsonify({"error": "Message is required"}), 400

        user_id = session["user_id"]

        # ── Create a new DB session if this is the first message ──
        is_new_session = False
        if not session_id:
            title      = message[:80] + ("…" if len(message) > 80 else "")
            session_id = create_chat_session(user_id, title)
            if not session_id:
                return jsonify({"error": "Could not create chat session"}), 500
            is_new_session = True

        # ── Save the user message ──
        save_message(session_id, user_id, "user", message)

        # ── Build conversation history for context ──
        history = get_session_messages(session_id)
        groq_messages = [
            {
                "role": "system",
                "content": (
                    "You are MAHADEV AI, an AI assistant made by Co-Member of Mahadev Group. "
                    "You are helpful, harmless, and honest. Use markdown formatting when appropriate."
                )
            }
        ]
        for m in history:
            groq_messages.append({"role": m["role"], "content": m["content"]})

        logger.info(f"[{session.get('username')}] session={session_id} msg={message[:50]}...")

        # ── Call Groq ──
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            max_tokens=1024,
            temperature=0.7
        )
        answer = response.choices[0].message.content

        # ── Save AI reply ──
        save_message(session_id, user_id, "assistant", answer)

        return jsonify({
            "response":       answer,
            "session_id":     session_id,
            "is_new_session": is_new_session,
        }), 200

    except Exception as e:
        logger.error(f"chat error: {e}")
        return jsonify({"error": "Failed to process request"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status":             "healthy",
        "api_configured":     bool(GROQ_API_KEY),
        "client_initialized": client is not None,
        "logged_in":          "user_id" in session,
    }), 200


# ─────────────────────────────────────────────
# STARTUP
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)