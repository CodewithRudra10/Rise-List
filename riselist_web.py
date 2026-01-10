import streamlit as st

# RiseList 🎯 - Final Stable Version (No Errors)
# Web Version v2.1 - Built by Rudra (Future CEO)
# January 2026

st.set_page_config(page_title="RiseList 🎯", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra")
st.markdown("---")

# Initialize tasks (must be before using them)
if "tasks" not in st.session_state:
    st.session_state.tasks = []

tasks = st.session_state.tasks

# Define functions FIRST (before using them)
def add_task():
    task_text = st.session_state.new_task.strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        st.success(f"✅ Added: {task_text}")
        st.session_state.new_task = ""
        st.rerun()
    else:
        st.warning("⚠️ Empty task skipped!")

def mark_done(index):
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        st.success("🎉 Task completed! Keep rising!")
        st.rerun()

def delete_task(index):
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        st.success(f"🗑️ Deleted: {removed['text']}")
        st.rerun()

# Sidebar - Add task
with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task", placeholder="e.g., Code for 1 hour")
    st.button("Add Task", on_click=add_task, type="primary", use_container_width=True)

# Main area - View tasks
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
st.caption("RiseList v2.1 — Built with ❤️ and Streamlit by Rudra")
st.caption("Keep grinding. You will rise.")
