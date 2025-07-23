from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import plotly.express as px
import os
import google.generativeai as genai  # Make sure this is installed

app = Flask(__name__)

# Set your Gemini API key
genai.configure(api_key="AIzaSyDOg3MwqjIIvKtDr1KMSHtXo2KXegn68f0")



# Load the Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")


# ---------- ROUTES ---------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    print("Question received:", question)

    sql = generate_sql_from_question(question)
    print("Generated SQL:", sql)

    result = query_database(sql)
    print("Query result:", result)

    return jsonify({
        "question": question,
        "generated_sql": sql,
        "result": result
    })

@app.route("/graph")
def show_graph():
    roas_path = generate_roas_chart()
    sales_path = generate_sales_chart()
    return render_template("graph.html", roas_chart=roas_path, sales_chart=sales_path)

# ---------- FUNCTIONS ---------- #
def generate_sql_from_question(question):
    prompt = f"""
You are an expert SQL assistant for an e-commerce system.

Generate only valid SQL queries (SQLite compatible), without markdown.

Available tables and columns:

1. total_sales(date, item_id, total_sales, total_units_ordered)
2. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
3. eligibility(date, item_id, is_eligible)

If asked to "Calculate the RoAS", use:
    ROAS = SUM(ad_sales) / SUM(ad_spend) from the ad_sales table.

Question: {question}
SQL:
"""
    try:
        response = model.generate_content(prompt)
        sql = response.text.strip()

        if sql.startswith("```sql"):
            sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql
    except Exception as e:
        return f"-- ERROR generating SQL: {str(e)}"

def query_database(sql):
    try:
        conn = sqlite3.connect("ecommerce_data.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return str(e)

def generate_roas_chart():
    conn = sqlite3.connect("ecommerce_data.db")
    df = pd.read_sql_query("SELECT date, ad_sales, ad_spend FROM ad_sales", conn)
    conn.close()

    df['date'] = pd.to_datetime(df['date'])
    df['roas'] = df['ad_sales'] / df['ad_spend']

    fig = px.line(df, x='date', y='roas', title='ROAS Over Time')
    output_path = "static/plots/roas_chart.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)

    return output_path.replace("static/", "")

def generate_sales_chart():
    conn = sqlite3.connect("ecommerce_data.db")
    df = pd.read_sql_query("SELECT date, total_sales FROM total_sales", conn)
    conn.close()

    df['date'] = pd.to_datetime(df['date'])

    fig = px.bar(df, x='date', y='total_sales', title='Total Sales Over Time')
    output_path = "static/plots/sales_chart.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)

    return output_path.replace("static/", "")

# ---------- MAIN ---------- #

if __name__ == "__main__":
    app.run(debug=True)
