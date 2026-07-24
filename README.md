# 🗄️ SQL Mastery - Interactive SQL Learning Platform

A complete web application for learning SQL from beginner to advanced levels. Built with **Python Flask** and **SQLite**, featuring a real database with sample data, interactive query execution, and progressive lessons.

![SQL Mastery](https://img.shields.io/badge/SQL-Learning-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Flask](https://img.shields.io/badge/Flask-3.0+-orange)

## ✨ Features

- 📚 **16 Progressive Lessons** - From `SELECT` basics to CTEs and window functions
- 💻 **Live SQL Playground** - Write and execute real queries against a SQLite database
- ✅ **Instant Validation** - Check if your solution matches the task requirements
- 📋 **Schema Explorer** - Browse all tables and columns while you learn
- 🎯 **Hints & Solutions** - Get help when stuck, reveal answers if needed
- 📊 **Progress Tracking** - Track your completion across all lessons
- 🎨 **Modern Dark UI** - Clean, responsive interface optimized for coding

## 📁 Project Structure

```
sql_learning_website/
├── app.py              # Main Flask application
├── database.py         # Database setup and query execution
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment config (Heroku/Railway)
├── runtime.txt        # Python version
├── README.md          # This file
├── templates/
│   └── index.html     # Main page template
└── static/
    ├── css/
    │   └── style.css  # Application styles
    └── js/
        └── app.js     # Frontend logic
```

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project:**
```bash
cd sql_learning_website
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser:**
Navigate to `http://localhost:5000`

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free)

1. Create a free account at [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo or upload the code
4. Use these settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**
6. Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Railway (Free Tier Available)

1. Sign up at [railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Python and deploys
5. Your app will be live at a `*.railway.app` domain

### Option 3: PythonAnywhere (Free)

1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to **Web** tab → **Add a new web app**
3. Select **Flask** and Python 3.9+
4. Upload your files via the **Files** tab
5. Update the WSGI file to point to your `app.py`
6. Reload the web app

### Option 4: Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login and create an app:
```bash
heroku login
heroku create your-sql-learning-app
```
3. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```
4. Open: `heroku open`

### Option 5: VPS / Cloud Server (DigitalOcean, AWS, GCP, etc.)

1. **Set up a server** with Python 3.9+
2. **Upload the project** via SCP/Git
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
5. **Set up Nginx** as a reverse proxy
6. **Point your domain** to the server IP

### Option 6: Custom Domain

After deploying to any platform:

1. **Buy a domain** from Namecheap, GoDaddy, Cloudflare, etc.
2. **Add DNS records:**
   - Type: `A` record
   - Name: `@` (root) or `www`
   - Value: Your server's IP address
3. **Configure SSL** (Let's Encrypt is free):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📖 Lesson Curriculum

### 🟢 Easy (5 lessons)
1. SELECT Basics
2. WHERE Clause
3. ORDER BY
4. DISTINCT & LIMIT
5. Pattern Matching (LIKE)

### 🟡 Medium (5 lessons)
1. Aggregate Functions
2. GROUP BY & HAVING
3. INNER JOIN
4. LEFT JOIN
5. Multiple JOINs

### 🔴 Advanced (6 lessons)
1. Subqueries
2. Self JOIN
3. Window Functions
4. CASE Expressions
5. CTEs (WITH clause)
6. Complex Real-World Query

## 🗃️ Database Schema

The app includes a realistic sample database with:
- **employees** (20 records) - with managers, departments, salaries
- **departments** (6 records) - with budgets and locations
- **projects** (10 records) - with status and timelines
- **employee_projects** (25 records) - many-to-many junction
- **customers** (12 records) - e-commerce data
- **products** (12 records) - with categories and prices
- **orders** (20 records) - with status tracking
- **order_items** (25 records) - line items

## 🔒 Security

- Only `SELECT` and `WITH` (CTE) queries are allowed
- All write operations (INSERT, UPDATE, DELETE, DROP, etc.) are blocked
- SQL injection is prevented via parameterized queries
- Session-based progress tracking

## 🛠️ Customization

### Adding New Lessons
Edit `app.py` and add to the `LESSONS` dictionary:

```python
"easy": [
    {
        "id": "e6",
        "title": "Your New Lesson",
        "description": "What they'll learn",
        "theory": "<h4>Title</h4><p>Explanation...</p>",
        "task": "What they need to do",
        "hint": "Helpful hint",
        "solution": "SELECT ... FROM ...",
        "tables": ["employees"],
        "validate": lambda cols, rows: len(rows) == expected_count
    }
]
```

### Adding New Tables
Edit `database.py` and add to `SCHEMA_SQL` and `INSERT_DATA_SQL`.

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

## 💬 Questions?

If you have any doubts about SQL concepts while using the app, feel free to ask!
