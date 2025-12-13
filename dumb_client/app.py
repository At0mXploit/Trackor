import streamlit as st
import requests
import uuid
from datetime import date

MCP_URL = "https://at0mxploit.fastmcp.app/mcp"

HEADERS = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN"  # only if private
}


def safe_post(payload):
    try:
        r = requests.post(MCP_URL, json=payload, headers=HEADERS, timeout=30)
    except Exception as e:
        return {"error": str(e)}

    if not r.text or not r.text.strip():
        return {"status_code": r.status_code, "message": "Empty response"}

    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "raw_response": r.text}


def call_tool(tool, params):
    return safe_post({
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {"name": tool, "arguments": params},
    })


def read_resource(uri):
    return safe_post({
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "resources/read",
        "params": {"uri": uri},
    })


st.set_page_config(page_title="Trackor Dumb MCP Client", layout="centered")
st.title("Trackor Dumb MCP Client")

# ---------------- Add Expense ----------------

st.header("Add Expense")

with st.form("add_expense"):
    d = st.date_input("Date", value=date.today(), key="add_date")
    amount = st.number_input("Amount", min_value=0.01, step=0.01, key="add_amount")
    category = st.text_input("Category", key="add_category")
    subcategory = st.text_input("Subcategory", key="add_subcategory")
    note = st.text_area("Note", key="add_note")

    if st.form_submit_button("Add Expense"):
        st.json(call_tool("add_expense", {
            "date": d.strftime("%Y-%m-%d"),
            "amount": amount,
            "category": category,
            "subcategory": subcategory,
            "note": note,
        }))

# ---------------- List Expenses ----------------

st.header("List Expenses")

if st.button("Fetch Expenses", key="list_expenses"):
    st.json(call_tool("list_expenses", {}))

# ---------------- Get Expense ----------------

st.header("Get Expense by ID")

get_id = st.number_input("Expense ID", min_value=1, step=1, key="get_id")
if st.button("Get Expense", key="get_btn"):
    st.json(call_tool("get_expense", {"expense_id": get_id}))

# ---------------- Update Expense ----------------

st.header("Update Expense")

with st.form("update_expense"):
    uid = st.number_input("Expense ID to Update", min_value=1, step=1, key="update_id")
    new_date = st.text_input("New Date (YYYY-MM-DD)", key="update_date")
    new_amount = st.text_input("New Amount", key="update_amount")
    new_category = st.text_input("New Category", key="update_category")
    new_subcategory = st.text_input("New Subcategory", key="update_subcategory")
    new_note = st.text_input("New Note", key="update_note")

    if st.form_submit_button("Update Expense"):
        payload = {"expense_id": uid}
        if new_date:
            payload["date"] = new_date
        if new_amount:
            payload["amount"] = float(new_amount)
        if new_category:
            payload["category"] = new_category
        if new_subcategory:
            payload["subcategory"] = new_subcategory
        if new_note:
            payload["note"] = new_note

        st.json(call_tool("update_expense", payload))

# ---------------- Delete Expense ----------------

st.header("Delete Expense")

delete_id = st.number_input("Expense ID to Delete", min_value=1, step=1, key="delete_id")
if st.button("Delete Expense", key="delete_btn"):
    st.json(call_tool("delete_expense", {"expense_id": delete_id}))

# ---------------- Delete by Date Range ----------------

st.header("Delete Expenses by Date Range")

start_date = st.date_input("Start Date", key="delete_start")
end_date = st.date_input("End Date", key="delete_end")

if st.button("Delete Range", key="delete_range"):
    st.json(call_tool("delete_expenses_by_date_range", {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }))

# ---------------- Summarize ----------------

st.header("Summarize Expenses")

sum_start = st.date_input("Summary Start Date", key="sum_start")
sum_end = st.date_input("Summary End Date", key="sum_end")
sum_category = st.text_input("Category (optional)", key="sum_category")
group_sub = st.checkbox("Group by Subcategory", key="sum_group")

if st.button("Run Summary", key="sum_btn"):
    payload = {
        "start_date": sum_start.strftime("%Y-%m-%d"),
        "end_date": sum_end.strftime("%Y-%m-%d"),
        "group_by_subcategory": group_sub,
    }
    if sum_category:
        payload["category"] = sum_category

    st.json(call_tool("summarize", payload))

# ---------------- Statistics ----------------

st.header("Overall Statistics")

if st.button("Get Statistics", key="stats_btn"):
    st.json(call_tool("get_statistics", {}))

# ---------------- Export ----------------

st.header("Export Expenses")

export_format = st.selectbox("Format", ["json", "csv"], key="export_format")
if st.button("Export", key="export_btn"):
    st.json(call_tool("export_expenses", {"format": export_format}))

# ---------------- Categories ----------------

st.header("Categories")

if st.button("Load Categories", key="categories_btn"):
    st.json(read_resource("expense://categories"))
