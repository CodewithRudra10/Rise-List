# RiseList 🎯 - With Permanent Save
# Web Version v2.0 - Built by Rudra
# January 2026
# One task at a time. Rise. Tasks now saved forever on your device!

import streamlit as st
from streamlit_local_storage import LocalStorage

localS = LocalStorage()

st.set_page_config(page_title="RiseList", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra — Class 9 student & Future CEO in training 💪")

# Key for localStorage
TASKS_KEY = "riselist_tasks"

# Load tasks from localStorage on start
saved_tasks = localS.getItem(TASKS_KEY)
if saved_tasks:
    tasks = eval(saved_tasks)  # Convert string back to list of dicts
else:
    tasks = []

# Save tasks whenever they change
def save_tasks():
    localS.setItem(TASKS_KEY, str(tasks))

# Functions
def add_task():
    task_text = st.session_state.new_task.strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        save_tasks()
        st.success(f"✅ Added: {task_text}")
        st.session_state.new_task = ""

def mark_done(index):
    tasks[index]["done"] = True
    save_tasks()
    st.success("🎉 Task completed!")

def delete_task(index):
    removed = tasks.pop(index)
    save_tasks()
    st.success(f"🗑️ Deleted: {removed['text']}")

# Sidebar
with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task")
    st.button("Add Task", on_click=add_task)

# Main view
st.header("📋 Your Tasks")

if not tasks:
    st.info("No tasks yet. Add one to start rising!")
else:
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
        status = "✓" if task["done"] else "○"
        with col1:
            if task["done"]:
                st.write(f"~~{i+1}. {task['text']}~~")
            else:
                st.write(f"{i+1}. {task['text']}")
        with col2:
            if not task["done"]:
                if st.button("Done", key=f"done_{i}"):
                    mark_done(i)
                    st.rerun()
        with col3:
            if st.button("Delete", key=f"del_{i}"):
                delete_task(i)
                st.rerun()

# Footer
st.markdown("---")
st.caption("RiseList v2.0 — Tasks saved permanently on your device 💾")
st.caption("Keep grinding. You will rise. Built with ❤️ by Rudra")
