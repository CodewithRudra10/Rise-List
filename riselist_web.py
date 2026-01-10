import streamlit as st
import time
import threading

# RiseList 🎯 - With Pomodoro Timer
# Web Version v2.1 - Built by Rudra (Future CEO)
# January 2026
# One task at a time. Rise. Now with focused work sessions!

st.set_page_config(page_title="RiseList 🎯", page_icon="🎯", layout="centered")

st.title("RiseList 🎯")
st.markdown("**One task at a time. Rise.**")
st.markdown("Built by Rudra — Class 9 student & Future CEO in training 💪")
st.markdown("---")

# Session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

tasks = st.session_state.tasks

# Pomodoro state
if "pomo_running" not in st.session_state:
    st.session_state.pomo_running = False
    st.session_state.pomo_time_left = 25 * 60  # 25 minutes in seconds
    st.session_state.pomo_phase = "work"  # "work" or "break"
    st.session_state.pomo_thread = None

# Pomodoro functions
def pomo_timer_thread():
    while st.session_state.pomo_running and st.session_state.pomo_time_left > 0:
        time.sleep(1)
        st.session_state.pomo_time_left -= 1
        # Update UI
        st.rerun()

def start_pomo():
    if not st.session_state.pomo_running:
        st.session_state.pomo_running = True
        st.session_state.pomo_thread = threading.Thread(target=pomo_timer_thread)
        st.session_state.pomo_thread.start()
        st.success("Pomodoro started! Focus time 💪")

def pause_pomo():
    st.session_state.pomo_running = False
    st.info("Pomodoro paused. Take a breath!")

def reset_pomo():
    st.session_state.pomo_running = False
    st.session_state.pomo_time_left = 25 * 60
    st.session_state.pomo_phase = "work"
    st.info("Pomodoro reset!")

# Sidebar - Add task + Pomodoro controls
with st.sidebar:
    st.header("➕ Add New Task")
    st.text_input("Enter task", key="new_task", placeholder="e.g., Code for 1 hour")
    st.button("Add Task", on_click=add_task, type="primary", use_container_width=True)

    st.markdown("---")
    st.header("🍅 Pomodoro Timer")
    mins, secs = divmod(st.session_state.pomo_time_left, 60)
    st.metric("Time Left", f"{mins:02d}:{secs:02d}", delta_color="off")
    st.caption(f"Phase: {'Work' if st.session_state.pomo_phase == 'work' else 'Break'}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start", type="primary", use_container_width=True):
            start_pomo()
    with col2:
        if st.button("Pause", type="secondary", use_container_width=True):
            pause_pomo()
    with col3:
        if st.button("Reset", type="secondary", use_container_width=True):
            reset_pomo()

# Main area - Tasks
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
