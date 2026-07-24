"""
SQL Learning Platform - Flask Application
A complete web application for learning SQL from easy to advanced.
"""
from flask import Flask, render_template, request, jsonify, session
import database as db
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sql-learning-dev-key-change-in-production')

# Initialize database on startup
@app.before_request
def ensure_db():
    if not os.path.exists(db.DATABASE_PATH):
        db.init_db()

@app.route("/")
def index():
    return render_template("index.html")

# Lesson data
LESSONS = {
    "easy": [
        {
            "id": "e1",
            "title": "SELECT Basics",
            "description": "Learn to retrieve data from tables",
            "theory": """
                <h4>SELECT Statement</h4>
                <p>The <code>SELECT</code> statement is the most fundamental SQL command. It retrieves data from one or more tables.</p>
                <div class="code-block">
SELECT * FROM employees;           -- All columns
SELECT name, salary FROM employees; -- Specific columns
                </div>
                <p><strong>Key points:</strong></p>
                <ul>
                    <li><code>*</code> means "all columns"</li>
                    <li>Column names are separated by commas</li>
                    <li>SQL statements end with a semicolon (optional in most databases)</li>
                </ul>
            """,
            "task": "Select the <strong>name</strong> and <strong>department</strong> of all employees from the employees table.",
            "hint": "Use: SELECT name, department FROM employees",
            "solution": "SELECT name, department FROM employees",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 20 and 'name' in cols and 'department' in cols and len(cols) == 2
        },
        {
            "id": "e2",
            "title": "WHERE Clause",
            "description": "Filter rows with conditions",
            "theory": """
                <h4>Filtering with WHERE</h4>
                <p>The <code>WHERE</code> clause filters rows based on conditions.</p>
                <div class="code-block">
SELECT * FROM employees WHERE department = 'Engineering';
SELECT * FROM employees WHERE salary > 80000;
SELECT * FROM employees WHERE age BETWEEN 25 AND 35;
                </div>
                <p><strong>Comparison operators:</strong> =, != or <>, >, <, >=, <=</p>
                <p><strong>Logical operators:</strong> AND, OR, NOT, IN, BETWEEN, LIKE</p>
            """,
            "task": "Find all employees in the <strong>Engineering</strong> department who earn more than <strong>90,000</strong>.",
            "hint": "Use AND to combine two conditions",
            "solution": "SELECT * FROM employees WHERE department = 'Engineering' AND salary > 90000",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 4 and all(r.get('department') == 'Engineering' and r.get('salary', 0) > 90000 for r in rows)
        },
        {
            "id": "e3",
            "title": "ORDER BY",
            "description": "Sort your results",
            "theory": """
                <h4>Sorting Results</h4>
                <p><code>ORDER BY</code> sorts the result set by one or more columns.</p>
                <div class="code-block">
SELECT * FROM employees ORDER BY salary DESC;
SELECT * FROM employees ORDER BY department ASC, salary DESC;
                </div>
                <p><strong>ASC</strong> = ascending (default), <strong>DESC</strong> = descending</p>
            """,
            "task": "List all employees ordered by salary from <strong>highest to lowest</strong>.",
            "hint": "Use ORDER BY with DESC",
            "solution": "SELECT * FROM employees ORDER BY salary DESC",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 20 and rows[0].get('salary', 0) >= rows[1].get('salary', 0)
        },
        {
            "id": "e4",
            "title": "DISTINCT & LIMIT",
            "description": "Remove duplicates and limit results",
            "theory": """
                <h4>DISTINCT and LIMIT</h4>
                <p><code>DISTINCT</code> removes duplicate values. <code>LIMIT</code> restricts the number of rows.</p>
                <div class="code-block">
SELECT DISTINCT department FROM employees;
SELECT * FROM employees LIMIT 5;
SELECT DISTINCT country FROM customers ORDER BY country LIMIT 10;
                </div>
            """,
            "task": "Get the <strong>unique list of departments</strong> that have employees.",
            "hint": "Use SELECT DISTINCT department FROM employees",
            "solution": "SELECT DISTINCT department FROM employees",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 5 and all(len(r) == 1 for r in rows)
        },
        {
            "id": "e5",
            "title": "Pattern Matching (LIKE)",
            "description": "Search with wildcards",
            "theory": """
                <h4>LIKE Operator</h4>
                <p><code>LIKE</code> is used for pattern matching with wildcards:</p>
                <ul>
                    <li><code>%</code> = matches any sequence of characters</li>
                    <li><code>_</code> = matches exactly one character</li>
                </ul>
                <div class="code-block">
SELECT * FROM employees WHERE name LIKE 'A%';    -- Names starting with A
SELECT * FROM employees WHERE name LIKE '%son';   -- Names ending with 'son'
SELECT * FROM customers WHERE city LIKE 'New%';   -- Cities starting with 'New'
                </div>
            """,
            "task": "Find all employees whose <strong>name starts with 'J'</strong>.",
            "hint": "Use LIKE 'J%'",
            "solution": "SELECT * FROM employees WHERE name LIKE 'J%'",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 3 and all(r.get('name', '').startswith('J') for r in rows)
        }
    ],
    "medium": [
        {
            "id": "m1",
            "title": "Aggregate Functions",
            "description": "COUNT, SUM, AVG, MIN, MAX",
            "theory": """
                <h4>Aggregate Functions</h4>
                <p>These functions compute a single value from a set of rows:</p>
                <div class="code-block">
SELECT COUNT(*) FROM employees;                    -- Total count
SELECT AVG(salary) FROM employees;                 -- Average
SELECT MAX(salary), MIN(salary) FROM employees;    -- Range
SELECT SUM(budget) FROM departments;               -- Total budget
                </div>
                <p>Common aggregates: <code>COUNT()</code>, <code>SUM()</code>, <code>AVG()</code>, <code>MIN()</code>, <code>MAX()</code></p>
            """,
            "task": "Find the <strong>average salary</strong> and <strong>total number of employees</strong>.",
            "hint": "Use AVG(salary) and COUNT(*) in one query",
            "solution": "SELECT AVG(salary) as avg_salary, COUNT(*) as total_employees FROM employees",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 1 and any('avg' in c.lower() for c in cols) and any('count' in c.lower() or 'total' in c.lower() for c in cols)
        },
        {
            "id": "m2",
            "title": "GROUP BY & HAVING",
            "description": "Group data and filter groups",
            "theory": """
                <h4>GROUP BY and HAVING</h4>
                <p><code>GROUP BY</code> groups rows that have the same values. <code>HAVING</code> filters these groups.</p>
                <div class="code-block">
SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_sal
FROM employees
GROUP BY department;

SELECT department, AVG(salary) as avg_sal
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;
                </div>
                <p><strong>WHERE</strong> filters rows <em>before</em> grouping. <strong>HAVING</strong> filters groups <em>after</em> grouping.</p>
            """,
            "task": "Find departments where the <strong>average salary is above 85,000</strong>, showing the department name and average salary.",
            "hint": "GROUP BY department HAVING AVG(salary) > 85000",
            "solution": "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department HAVING AVG(salary) > 85000",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) >= 3 and all(r.get('avg_salary', r.get('AVG(salary)', 0)) > 85000 for r in rows)
        },
        {
            "id": "m3",
            "title": "INNER JOIN",
            "description": "Combine data from two tables",
            "theory": """
                <h4>INNER JOIN</h4>
                <p>Returns only rows where there is a match in both tables.</p>
                <div class="code-block">
SELECT e.name, d.name AS dept_name, d.location
FROM employees e
INNER JOIN departments d ON e.department = d.name;
                </div>
                <p><strong>Table aliases</strong> (e, d) make queries shorter and clearer.</p>
            """,
            "task": "List each <strong>employee's name</strong> along with their <strong>department's location</strong>.",
            "hint": "JOIN employees with departments on the department name",
            "solution": "SELECT e.name, d.location FROM employees e INNER JOIN departments d ON e.department = d.name",
            "tables": ["employees", "departments"],
            "validate": lambda cols, rows: len(rows) == 20 and any('location' in c.lower() for c in cols)
        },
        {
            "id": "m4",
            "title": "LEFT JOIN",
            "description": "Include all rows from the left table",
            "theory": """
                <h4>LEFT JOIN</h4>
                <p>Returns ALL rows from the left table, and matched rows from the right. Unmatched right-side values are NULL.</p>
                <div class="code-block">
SELECT d.name, COUNT(e.id) as emp_count
FROM departments d
LEFT JOIN employees e ON d.name = e.department
GROUP BY d.name;
                </div>
                <p>Useful when you want to see ALL categories, even those with zero matches.</p>
            """,
            "task": "Show <strong>all departments</strong> and the <strong>count of employees</strong> in each (including departments with 0 employees).",
            "hint": "Use LEFT JOIN from departments to employees, then GROUP BY",
            "solution": "SELECT d.name, COUNT(e.id) as employee_count FROM departments d LEFT JOIN employees e ON d.name = e.department GROUP BY d.name",
            "tables": ["departments", "employees"],
            "validate": lambda cols, rows: len(rows) == 6 and any('count' in c.lower() for c in cols)
        },
        {
            "id": "m5",
            "title": "Multiple JOINs",
            "description": "Join three or more tables",
            "theory": """
                <h4>Joining Multiple Tables</h4>
                <p>You can chain multiple JOINs to combine data from several tables.</p>
                <div class="code-block">
SELECT e.name, p.name AS project_name, ep.hours_worked
FROM employees e
INNER JOIN employee_projects ep ON e.id = ep.emp_id
INNER JOIN projects p ON ep.project_id = p.id;
                </div>
            """,
            "task": "List employees who work on projects, showing the <strong>employee name</strong>, <strong>project name</strong>, and <strong>hours worked</strong>.",
            "hint": "Join employees → employee_projects → projects",
            "solution": "SELECT e.name, p.name as project_name, ep.hours_worked FROM employees e INNER JOIN employee_projects ep ON e.id = ep.emp_id INNER JOIN projects p ON ep.project_id = p.id",
            "tables": ["employees", "employee_projects", "projects"],
            "validate": lambda cols, rows: len(rows) == 25 and any('project' in c.lower() for c in cols) and any('hours' in c.lower() for c in cols)
        }
    ],
    "advanced": [
        {
            "id": "a1",
            "title": "Subqueries",
            "description": "Queries within queries",
            "theory": """
                <h4>Subqueries</h4>
                <p>A query nested inside another query. Can be used in SELECT, WHERE, or FROM.</p>
                <div class="code-block">
-- Employees earning above average
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Departments with above-average budgets
SELECT name FROM departments
WHERE budget > (SELECT AVG(budget) FROM departments);
                </div>
            """,
            "task": "Find employees who earn <strong>more than the company average salary</strong>.",
            "hint": "WHERE salary > (SELECT AVG(salary) FROM employees)",
            "solution": "SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) >= 6 and all(r.get('salary', 0) > 87000 for r in rows)
        },
        {
            "id": "a2",
            "title": "Self JOIN",
            "description": "Join a table to itself",
            "theory": """
                <h4>Self JOIN</h4>
                <p>Joining a table to itself using aliases. Perfect for hierarchical data.</p>
                <div class="code-block">
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
                </div>
                <p>Notice both tables are <code>employees</code> — we use aliases to distinguish them.</p>
            """,
            "task": "List each <strong>employee with their manager's name</strong>. Include employees who don't have a manager.",
            "hint": "Use LEFT JOIN employees with itself: e.manager_id = m.id",
            "solution": "SELECT e.name as employee, m.name as manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.id",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 20 and any('manager' in c.lower() for c in cols)
        },
        {
            "id": "a3",
            "title": "Window Functions",
            "description": "ROW_NUMBER, RANK, DENSE_RANK",
            "theory": """
                <h4>Window Functions</h4>
                <p>Perform calculations across a set of rows related to the current row.</p>
                <div class="code-block">
SELECT name, department, salary,
  RANK() OVER (ORDER BY salary DESC) as overall_rank,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
                </div>
                <p><strong>PARTITION BY</strong> divides rows into groups. <strong>ORDER BY</strong> determines the ranking order.</p>
            """,
            "task": "Rank employees by salary <strong>within each department</strong> using RANK().",
            "hint": "Use PARTITION BY department in the OVER clause",
            "solution": "SELECT name, department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank FROM employees",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 20 and any('rank' in c.lower() for c in cols)
        },
        {
            "id": "a4",
            "title": "CASE Expressions",
            "description": "Conditional logic in SQL",
            "theory": """
                <h4>CASE Expressions</h4>
                <p>Add conditional logic to your queries, similar to if-then-else.</p>
                <div class="code-block">
SELECT name, salary,
  CASE
    WHEN salary >= 120000 THEN 'Senior'
    WHEN salary >= 90000 THEN 'Mid-Level'
    WHEN salary >= 70000 THEN 'Junior'
    ELSE 'Entry'
  END AS level
FROM employees;
                </div>
            """,
            "task": "Categorize employees: <strong>'Senior'</strong> (≥120k), <strong>'Mid'</strong> (≥90k), <strong>'Junior'</strong> (≥70k), or <strong>'Entry'</strong>.",
            "hint": "Use nested WHEN clauses with CASE",
            "solution": "SELECT name, salary, CASE WHEN salary >= 120000 THEN 'Senior' WHEN salary >= 90000 THEN 'Mid' WHEN salary >= 70000 THEN 'Junior' ELSE 'Entry' END as level FROM employees",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 20 and any('level' in c.lower() for c in cols) and any(r.get('level') == 'Senior' for r in rows)
        },
        {
            "id": "a5",
            "title": "CTEs (WITH clause)",
            "description": "Common Table Expressions",
            "theory": """
                <h4>Common Table Expressions (CTEs)</h4>
                <p>Temporary named result sets that make complex queries more readable.</p>
                <div class="code-block">
WITH high_earners AS (
  SELECT * FROM employees WHERE salary > 100000
)
SELECT department, COUNT(*) as count
FROM high_earners
GROUP BY department;
                </div>
                <p>CTEs can also be <strong>recursive</strong> for hierarchical data.</p>
            """,
            "task": "Use a CTE to find departments with more than 4 employees, then show the department name and employee count.",
            "hint": "WITH dept_counts AS (SELECT department, COUNT(*) as cnt FROM employees GROUP BY department) SELECT * FROM dept_counts WHERE cnt > 4",
            "solution": "WITH dept_counts AS (SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department) SELECT * FROM dept_counts WHERE emp_count > 4",
            "tables": ["employees"],
            "validate": lambda cols, rows: len(rows) == 3 and all(r.get('emp_count', r.get('COUNT(*)', 0)) > 4 for r in rows)
        },
        {
            "id": "a6",
            "title": "Complex Real-World Query",
            "description": "Combine everything you've learned",
            "theory": """
                <h4>Putting It All Together</h4>
                <p>Real-world queries often combine JOINs, aggregates, subqueries, and window functions.</p>
                <div class="code-block">
-- Top 3 customers by total order value
SELECT c.name, c.country, SUM(o.total_amount) as total_spent,
  RANK() OVER (ORDER BY SUM(o.total_amount) DESC) as rank
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 3;
                </div>
            """,
            "task": "Find the <strong>top 3 customers by total order amount</strong> (only 'Delivered' orders), showing customer name and total spent.",
            "hint": "JOIN customers and orders, filter by status='Delivered', GROUP BY customer, ORDER BY total DESC, LIMIT 3",
            "solution": "SELECT c.name, SUM(o.total_amount) as total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE o.status = 'Delivered' GROUP BY c.id ORDER BY total_spent DESC LIMIT 3",
            "tables": ["customers", "orders"],
            "validate": lambda cols, rows: len(rows) == 3 and rows[0].get('total_spent', 0) >= rows[1].get('total_spent', 0)
        }
    ]
}

# For API: flatten lessons
ALL_LESSONS = []
for level, items in LESSONS.items():
    for item in items:
        item['level'] = level
        ALL_LESSONS.append(item)

@app.route("/api/lessons")
def get_lessons():
    return jsonify(LESSONS)

@app.route("/api/execute", methods=["POST"])
def execute_sql():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "No query provided", "columns": [], "rows": []})

    # Security: Only allow SELECT statements
    # Remove comments first
    query_clean = re.sub(r'--[^
]*', '', query)
    query_clean = re.sub(r'/\*.*?\*/', '', query_clean, flags=re.DOTALL)
    query_clean = query_clean.strip()

    # Check if it's a SELECT or WITH (for CTEs)
    first_word = query_clean.split()[0].upper() if query_clean.split() else ""

    if first_word not in ("SELECT", "WITH"):
        return jsonify({
            "error": "Only SELECT and WITH (CTE) queries are allowed for security. This is a learning environment.",
            "columns": [],
            "rows": []
        })

    # Additional check: no dangerous keywords
    dangerous = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
    upper_query = query_clean.upper()
    for word in dangerous:
        if re.search(r'\b' + word + r'\b', upper_query):
            return jsonify({
                "error": f"'{word}' statements are not allowed. This is a read-only learning environment.",
                "columns": [],
                "rows": []
            })

    result = db.execute_query(query)
    return jsonify(result)

@app.route("/api/validate", methods=["POST"])
def validate_solution():
    data = request.get_json()
    lesson_id = data.get("lesson_id")
    query = data.get("query", "").strip()

    lesson = next((l for l in ALL_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return jsonify({"correct": False, "message": "Lesson not found"})

    # Execute the query
    result = db.execute_query(query)
    if result["error"]:
        return jsonify({"correct": False, "message": f"Query error: {result['error']}"})

    # Validate
    try:
        is_correct = lesson["validate"](result["columns"], result["rows"])
        if is_correct:
            # Track progress in session
            progress = session.get("progress", [])
            if lesson_id not in progress:
                progress.append(lesson_id)
                session["progress"] = progress
            return jsonify({
                "correct": True,
                "message": "✅ Correct! Great job! Move on to the next lesson.",
                "columns": result["columns"],
                "rows": result["rows"]
            })
        else:
            return jsonify({
                "correct": False,
                "message": "❌ Not quite right. Check your query against the task requirements.",
                "columns": result["columns"],
                "rows": result["rows"]
            })
    except Exception as e:
        return jsonify({
            "correct": False,
            "message": f"Validation error: {str(e)}",
            "columns": result["columns"],
            "rows": result["rows"]
        })

@app.route("/api/progress")
def get_progress():
    return jsonify(session.get("progress", []))

@app.route("/api/schema")
def get_schema():
    """Return database schema for display."""
    conn = db.get_db_connection()
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = cursor.fetchall()

    schema = {}
    for table in tables:
        table_name = table["name"]
        cols = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        schema[table_name] = [{"name": c["name"], "type": c["type"]} for c in cols]

    conn.close()
    return jsonify(schema)

if __name__ == "__main__":
    # Initialize DB if needed
    if not os.path.exists(db.DATABASE_PATH):
        db.init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
