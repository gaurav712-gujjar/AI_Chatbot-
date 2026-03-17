# ✦ MAHADEV AI — Intelligent Chat Assistant

> A full-stack AI chatbot powered by **Groq (Llama 3.3-70B)**, built with **Flask** and **MySQL**, featuring user authentication, persistent chat history, and a modern dark UI.

---

## 📸 Features

- 🤖 **AI Chat** — Powered by Llama 3.3-70B via Groq API with streaming effect
- 🔐 **Authentication** — Register, Login, Logout with secure password hashing
- 💾 **Chat Persistence** — All messages and sessions saved to MySQL database
- 🎨 **Modern UI** — Dark theme with animated background, markdown rendering, syntax highlighting
- 📱 **Responsive** — Works on desktop and mobile
- 🔒 **Secure** — Sessions, CSRF-safe forms, no secrets in code

---

## 🗂️ Project Structure

```
mahadev-ai/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile                # For Railway/Render deployment
├── schema.sql              # MySQL database schema
├── .env                    # Secret keys (DO NOT upload to GitHub)
├── .gitignore              # Files to ignore in Git
├── README.md               # This file
└── templates/
    ├── index.html          # Main chat interface
    ├── login.html          # Login page
    └── register.html       # Register page
```

---

## 🗄️ Database Schema

```
users
 ├── id, first_name, last_name, username
 ├── email, password_hash
 └── created_at, updated_at

chat_sessions
 ├── id, user_id (→ users)
 ├── title
 └── created_at, updated_at

chat_messages
 ├── id, session_id (→ chat_sessions), user_id (→ users)
 ├── role (user / assistant)
 ├── content
 └── created_at
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/mahadev-ai.git
cd mahadev-ai
```

### 2. Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a file named `.env` in the project root:

```env
# Groq AI
GROQ_API_KEY=gsk_your_groq_api_key_here

# Flask
SECRET_KEY=any_long_random_string_here

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=mahadev_ai
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Set up the database

**Option A — Auto setup (recommended):**
Just run the app — `init_db()` creates all tables automatically on first startup.

**Option B — Manual:**
```bash
mysql -u root -p < schema.sql
```

### 6. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## 🚀 Deploy to Railway (Free)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mahadev-ai.git
git push -u origin main
```

### Step 2 — Deploy on Railway

1. Go to [railway.app](https://railway.app) → Login with GitHub
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `mahadev-ai` repository
4. Click **Deploy Now**

### Step 3 — Add MySQL Database

1. In your Railway project → Click **New**
2. Click **Database** → **Add MySQL**
3. Railway creates the database automatically

### Step 4 — Set Environment Variables

In your Flask service → **Variables** tab, add:

| Variable | Value |
|---|---|
| `GROQ_API_KEY` | your Groq key |
| `SECRET_KEY` | any random string |
| `MYSQL_HOST` | reference from MySQL service |
| `MYSQL_PORT` | reference from MySQL service |
| `MYSQL_USER` | reference from MySQL service |
| `MYSQL_PASSWORD` | reference from MySQL service |
| `MYSQL_DATABASE` | reference from MySQL service |

### Step 5 — Get Your Live URL

Go to your Flask service → **Settings** → **Networking** → **Generate Domain**

Your app is live! 🎉

---

## 🔑 Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for AI | `gsk_abc123...` |
| `SECRET_KEY` | Flask session secret | `random_string_here` |
| `MYSQL_HOST` | MySQL server host | `localhost` |
| `MYSQL_PORT` | MySQL server port | `3306` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | `yourpassword` |
| `MYSQL_DATABASE` | Database name | `mahadev_ai` |

---

## 📦 Requirements

```
Flask==3.0.0
flask-cors==4.0.0
groq==0.9.0
mysql-connector-python==8.3.0
python-dotenv==1.0.0
httpx==0.27.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🔒 Security Notes

- ✅ Passwords are hashed with SHA-256 + random salt
- ✅ Sessions are secured with `SECRET_KEY`
- ✅ `.env` is git-ignored — secrets never go to GitHub
- ✅ All chat routes require login (`@login_required`)
- ⚠️ For production, consider switching to `bcrypt` for stronger password hashing

---

## 🛠️ API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/` | Chat interface | ✅ Yes |
| GET | `/login` | Login page | ❌ No |
| POST | `/login` | Process login | ❌ No |
| GET | `/register` | Register page | ❌ No |
| POST | `/register` | Create account | ❌ No |
| GET | `/logout` | Sign out | ✅ Yes |
| POST | `/chat` | Send message to AI | ✅ Yes |
| GET | `/api/sessions` | Get user's chat sessions | ✅ Yes |
| GET | `/api/sessions/<id>/messages` | Get messages in a session | ✅ Yes |
| GET | `/api/health` | Health check | ❌ No |

---

## 💡 How Chat Persistence Works

```
User sends message
        ↓
Does session_id exist?
   No  → Create new row in chat_sessions
   Yes → Use existing session
        ↓
Save user message → chat_messages (role: "user")
        ↓
Fetch full message history from DB
        ↓
Send history to Groq API (AI has full context)
        ↓
Save AI reply → chat_messages (role: "assistant")
        ↓
Return response to browser
```

---

## 📊 Storage Estimates

| Users | Messages/month | Storage/month |
|---|---|---|
| 10 | ~5,000 | ~15 MB |
| 100 | ~50,000 | ~150 MB |
| 1,000 | ~500,000 | ~1.5 GB |

Check actual DB size anytime:
```sql
SELECT table_name,
       ROUND((data_length + index_length) / 1024, 2) AS size_kb
FROM information_schema.tables
WHERE table_schema = 'mahadev_ai';
```

---

## 🔄 Updating After Deployment

After any code change:
```bash
git add .
git commit -m "describe your change"
git push
```
Railway auto-detects the push and redeploys in ~1–2 minutes.

---

## 🤝 Made By

**MAHADEV GROUP** — AI-powered tools built for everyone.

---

## 📄 License

This project is for personal and educational use.