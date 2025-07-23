# 🛒 SmartCart AI – E-commerce Data Chatbot with Visualizations

This project is a beginner-friendly **Flask web app** that uses **Gemini AI** to generate SQL queries from natural language questions and answers them using data from an e-commerce dataset (CSV → SQLite). It also includes visualizations for ROAS and Total Sales.

---

## ✨ Features

- 🤖 Ask natural questions like:
  - “What is my total sales?”
  - “Calculate the ROAS”
  - “Which product had the highest CPC?”
- 🧠 Uses **Gemini AI** to convert question → SQL
- 💬 Returns:
  - ✅ Generated SQL query
  - ✅ Executed result from SQLite database
- 📊 Separate visualization page:
  - ROAS over time
  - Total sales over time

---

## 🗂️ Project Structure
ecom_ai/
├── app.py # Main Flask backend
├── ecommerce_data.db # SQLite DB created from CSVs
├── templates/
│ ├── index.html # Chatbot frontend
│ └── graph.html # Visualization page
├── static/
│ └── plots/ # Generated charts (ROAS, sales)
├── import_csv_to_sqlite.py # CSV → SQLite converter
├── README.md # You are here



