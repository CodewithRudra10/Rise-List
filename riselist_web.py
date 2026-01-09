import streamlit as st
import json

# RiseList 🎯 - Permanent Save (URL-based)
# Web Version v2.0 - Built by Rudra 
# January 2026
# One task at a time. Rise. Tasks saved in URL!

st.set_page_config(page_title="RiseList 🎯", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra — Class 9 student & Future CEO in training 💪")
st.markdown("---")

# Load tasks from URL query params
query_params = st.query_params
saved_tasks = query_params.get("tasks", [None])[0]

if saved_tasks:
    try:
        tasks = json.loads(saved_tasks)
    except:
        tasks = []
else:
    tasks = []

# Save tasks to URL
def save_to_url():
    st.query_params["tasks"] = json.dumps(tasks)

# Functions
def add_task():
    task_text = st.session_state.new_task.strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        save_to_url()
        st.success(f"✅ Added: {task_text}")
        st.session_state.new_task = ""
        st.rerun()

def mark_done(index):
    tasks[index]["done"] = True
    save_to_url()
    st.success("🎉 Task completed!")
    st.rerun()

def delete_task(index):
    tasks.pop(index)
    save_to_url()
    st.success("🗑️ Task deleted!")
    st.rerun()

# Sidebar
with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task", placeholder="e.g., Study Python")
    st.button("Add Task", on_click=add_task, type="primary")

# Main view
st.header("📋 Your Tasks")

if not tasks:
    st.info("No tasks yet. Add one to start rising! 🚀")
else:
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            if task["done"]:
                st.write(f"~~{i+1}. {task['text']}~~ ✅")
            else:
                st.write(f"{i+1}. ○ {task['text']}")
        with col2:
            if not task["done"]:
                if st.button("Done", key=f"done_{i}"):
                    mark_done(i)
        with col3:
            if st.button("Delete", key=f"del_{i}"):
                delete_task(i)

# Footer
st.markdown("---")
st.caption("RiseList v2.0 — Tasks saved in URL (copy link to share/save)")
st.caption("Keep grinding. You will rise. Built with ❤️ by Rudra")
