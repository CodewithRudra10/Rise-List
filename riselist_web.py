import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ====================
# Task Class
# ====================
class Task:
    def __init__(self, title, priority, due_date=None):
        self.title = title
        self.priority = priority
        self.done = False
        self.due_date = due_date if due_date else "No due date"

    def __str__(self):
        status = "✅ Done" if self.done else "⏳ Pending"
        due = f" | Due: {self.due_date}" if self.due_date != "No due date" else ""
        return f"{status} {self.title} (Priority: {self.priority}){due}"

# ====================
# TaskManager Class (handles tasks + persistence)
# ====================
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()

    def add_task(self, title, priority, due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True
            self.save_tasks()
            return self.tasks[index]
        return None

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            return removed
        return None

    def clear_all(self):
        self.tasks = []
        self.save_tasks()

    def show_all(self):
        if not self.tasks:
            st.info("No tasks yet — add one to get started!")
            return

        for i, task in enumerate(self.tasks):
            st.write(f"{i+1}. {task}")

    def save_tasks(self):
        data = [
            {
                "title": t.title,
                "priority": t.priority,
                "done": t.done,
                "due_date": t.due_date if t.due_date != "No due date" else None
            }
            for t in self.tasks
        ]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                self.tasks = []
                for item in data:
                    task = Task(
                        item["title"],
                        item["priority"],
                        item.get("due_date")
                    )
                    task.done = item.get("done", False)
                    self.tasks.append(task)
            except Exception as e:
                st.error(f"Error loading tasks: {e}")
        # else: no file → start empty

# ====================
# Main App
# ====================
st.set_page_config(page_title="RiseList", layout="wide")

# Logo at the top
logo_path = "riselist-logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=220, use_column_width="auto")
else:
    st.caption("[Upload riselist-logo.png to repo]")

st.title("RiseList – Rise Every Day")
st.caption("Your personal task manager • Built by Rudra")

# Load or create manager
if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()

manager = st.session_state.manager

# === Add new task ===
st.subheader("Add a Task")
col1, col2, col3 = st.columns([3, 1.5, 2])
new_title = col1.text_input("Task Title", placeholder="e.g. Study Physics")
priority = col2.selectbox("Priority", ["High", "Medium", "Low"])
due_date = col3.date_input("Due Date (optional)", value=None)

if st.button("➕ Add Task", type="primary") and new_title.strip():
    due_str = due_date.strftime("%Y-%m-%d") if due_date else None
    added = manager.add_task(new_title.strip(), priority, due_str)
    st.success(f"🎉 Task '{added.title}' added successfully!")
    st.balloons()

# === Display Tasks ===
st.subheader("Your Tasks")
if not manager.tasks:
    st.info("No tasks yet — add one above!")
else:
    cols = st.columns([5, 1, 1])
    for i, task in enumerate(manager.tasks):
        with cols[0]:
            st.markdown(task)
        with cols[1]:
            if st.button("✅ Done", key=f"done_{i}"):
                manager.mark_done(i)
                st.rerun()
        with cols[2]:
            if st.button("🗑️ Delete", key=f"del_{i}"):
                manager.delete_task(i)
                st.rerun()

# === Weekly Calendar ===
st.subheader("Weekly Progress")
today = datetime.now().date()
week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)

week_tasks = [
    t for t in manager.tasks
    if t.due_date != "No due date"
    and week_start <= datetime.strptime(t.due_date, "%Y-%m-%d").date() <= week_end
]

if not week_tasks:
    st.info(f"No tasks scheduled from {week_start} to {week_end}")
else:
    st.write(f"**Week: {week_start} → {week_end}**")
    for task in week_tasks:
        st.markdown(f"- {task}")

# Footer
st.markdown("---")
st.caption("RiseList v2.1 — Built with ❤️ and Streamlit")
st.caption("Keep rising. You got this!")
