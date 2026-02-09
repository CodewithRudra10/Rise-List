import streamlit as st
import json
import os

# === Paste your Task + TaskManager code here (the block you shared) ===
class Task:
    def __init__(self, title, priority):
        self.title = title
        self.priority = priority
        self.done = False

    def __str__(self):
        status = "Done" if self.done else "Pending"
        return f"[{status}] {self.title} (Priority: {self.priority})"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()  # auto-load on start

    def add_task(self, title, priority):
        task = Task(title, priority)
        self.tasks.append(task)
        self.save_tasks()
        st.success(f"Added: {task}")

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True
            self.save_tasks()
            st.success(f"Marked '{self.tasks[index].title}' as Done!")

    def show_all(self):
        if not self.tasks:
            st.info("No tasks yet — add one!")
        else:
            for i, task in enumerate(self.tasks):
                st.write(f"{i+1}. {task}")

    def save_tasks(self):
        data = [
            {
                "title": t.title,
                "priority": t.priority,
                "done": t.done
            } for t in self.tasks
        ]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Tasks saved!✅")  # for console debug

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
            self.tasks = []
            for item in data:
                task = Task(item["title"], item["priority"])
                task.done = item["done"]
                self.tasks.append(task)
            print("Tasks loaded!")
        else:
            print("No saved tasks yet.")

# === Streamlit App UI starts here ===
st.title("RiseList – Rise Every Day")
# === RiseList Logo (top of page) ===
logo_path = "RiseList logo.img.png"

if os.path.exists(logo_path):
    st.image(logo_path, width=180, use_column_width="auto", caption="RiseList – Rise Every Day")
else:
    st.caption("[Logo missing – upload riselist-logo.png to repo]")

# Create or load the manager (use session_state to keep it between reruns)
if "task_manager" not in st.session_state:
    st.session_state.task_manager = TaskManager()

manager = st.session_state.task_manager

# Input for new task
col1, col2 = st.columns([3, 1])
with col1:
    new_title = st.text_input("New Task", placeholder="e.g. Add a Task to get Started!")
with col2:
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add Task") and new_title:
    manager.add_task(new_title, priority)

# Show all tasks
st.subheader("Your Tasks")
manager.show_all()

# Mark done (simple index input — can improve later)
done_index = st.number_input("Mark task as Done (enter number)", min_value=0, step=1)
if st.button("Mark Done") and 0 <= done_index < len(manager.tasks):
    manager.mark_done(done_index)
    
    print("---------Thanks for Using RiseList!-----------")

# Footer
st.markdown("---")
st.caption("RiseList v2.1 — Built with ❤️ and Streamlit by Rudra")
st.caption("Keep grinding. You will rise.")
