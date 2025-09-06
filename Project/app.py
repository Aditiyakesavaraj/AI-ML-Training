import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()
API_KEY = os.getenv("XAI_API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.x.ai/v1")

app = Flask(__name__, template_folder="templates")

def invoke_grok(prompt, model="grok-3"):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant that converts natural language to SQL and formats answers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )
    return resp.choices[0].message.content

# --- Run SQL on SQLite ---
def run_sql_and_fetch(sql):
    conn = sqlite3.connect("plans.db")
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Exception as e:
        rows = []
    conn.close()
    return rows

# --- Home Page ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Chat API ---
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    # Step 1: Convert user query → SQL
    sql_prompt = f"Convert this user request into valid SQL (SQLite) for table 'plans': {user_msg}"
    sql_query = invoke_grok(sql_prompt)
    print("DEBUG SQL:", sql_query)

    # Step 2: Run SQL on DB
    results = run_sql_and_fetch(sql_query)

    if not results:
        reply = "Sorry, no matching plan found."
    else:
        # Step 3: Format nicely
        format_prompt = f"Format this telecom plan result in a user-friendly way: {results}"
        reply = invoke_grok(format_prompt)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
