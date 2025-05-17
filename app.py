
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Fair Game Cost Calculator", layout="centered")

st.title("🎮 Fair Game Time Cost Calculator")
st.markdown("Easily calculate the fair cost for each player based on their play time and shared usage.")

with st.form("player_form"):
    st.markdown("## ⏱ Enter Player Times and Rate")

    hourly_rate = st.number_input("Hourly Rate (EGP)", min_value=10, max_value=500, value=85, step=5)
    rate_per_min = hourly_rate / 60

    num_players = st.number_input("Number of Players", min_value=1, max_value=20, value=4)
    players = []

    for i in range(num_players):
        with st.expander(f"Player {i+1} Details"):
            name = st.text_input(f"Player {i+1} Name", value=f"Player{i+1}", key=f"name_{i}")
            col1, col2 = st.columns(2)
            start = col1.time_input("Start Time", key=f"start_{i}")
            end = col2.time_input("End Time", key=f"end_{i}")
            players.append({"name": name, "start": start, "end": end})

    submitted = st.form_submit_button("Calculate Cost")

if submitted:
    def to_datetime_range(start_time, end_time):
        today = datetime.today()
        start_dt = datetime.combine(today, start_time)
        end_dt = datetime.combine(today, end_time)
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)
        return start_dt, end_dt

    player_times = []
    for p in players:
        start_dt, end_dt = to_datetime_range(p["start"], p["end"])
        player_times.append({
            "name": p["name"],
            "start": start_dt,
            "end": end_dt
        })

    min_time = min(p["start"] for p in player_times)
    max_time = max(p["end"] for p in player_times)

    timeline = {}
    durations = {}
    current_time = min_time
    while current_time < max_time:
        present = [
            p["name"]
            for p in player_times
            if p["start"] <= current_time < p["end"]
        ]
        if present:
            for name in present:
                durations[name] = durations.get(name, 0) + 1
            timeline[current_time] = present
        current_time += timedelta(minutes=1)

    st.markdown("## 💰 Cost Breakdown")
    for name in durations:
        total_minutes = durations[name]
        total_cost = 0
        for time, present in timeline.items():
            if name in present:
                total_cost += rate_per_min / len(present)
        st.write(f"**{name}**: {total_cost:.2f} EGP for {total_minutes} minutes")
