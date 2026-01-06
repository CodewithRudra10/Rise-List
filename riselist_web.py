import streamlit as st

st.set_page_config(page_title="RiseList 🎯", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra — 💪")
st.markdown("---")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

tasks = st.session_state.tasks

def add_task():
    task_text = st.session_state.new_task.strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        st.success(f"✅ Added: {task_text}")
        st.session_state.new_task = ""
        st.rerun()

def mark_done(index):
    tasks[index]["done"] = True
    st.success("🎉 Task completed!")
    st.rerun()

def delete_task(index):
    removed = tasks.pop(index)
    st.success(f"🗑️ Deleted: {removed['text']}")
    st.rerun()

with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task")
    st.button("Add Task", on_click=add_task)

st.header("📋 Your Tasks")

if not tasks:
    st.info("No tasks yet. Add one to start rising!")
else:
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
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

st.markdown("---")
st.caption("RiseList v1.0 — Built with ❤️ by Rudra")
st.caption("Keep grinding. You will rise.")
