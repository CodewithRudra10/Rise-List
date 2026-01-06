import streamlit as st

# RiseList 🎯
# Web Version v1.0 - Built by Rudra 
# January 2026
# One task at a time. Rise.

st.set_page_config(page_title="RiseList", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra — Class 9 student & Future CEO in training 💪")

# Initialize tasks in session state (so they remember while app is open)
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Functions
def add_task():
    task_text = st.session_state.new_task.strip()
    if task_text:
        st.session_state.tasks.append({"text": task_text, "done": False})
        st.success(f"✅ Added: {task_text}")
        st.session_state.new_task = ""  # Clear input
    else:
        st.warning("⚠️ Empty task skipped!")

def mark_done(index):
    st.session_state.tasks[index]["done"] = True
    st.success("🎉 Task marked done!")

def delete_task(index):
    removed = st.session_state.tasks.pop(index)
    st.success(f"🗑️ Deleted: {removed['text']}")

# Sidebar for adding task
with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task")
    st.button("Add Task", on_click=add_task)

# Main area - View tasks
st.header("📋 Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one in the sidebar to start rising!")
else:
    for i, task in enumerate(st.session_state.tasks):
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
        with col3:
            if st.button("Delete", key=f"del_{i}"):
                delete_task(i)

# Footer
st.markdown("---")
st.caption("RiseList v1.0 — Built with ❤️ and Streamlit by Rudra")
st.caption("Keep grinding. You will rise.")