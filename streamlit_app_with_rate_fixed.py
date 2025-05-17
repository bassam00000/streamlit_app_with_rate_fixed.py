
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
    def to_datetime(t):
        return datetime.combine(datetime.today(), t)

    min_time = min(to_datetime(p["start"]) for p in players)
    max_time = max(to_datetime(p["end"]) for p in players)

    timeline = {}
    durations = {}
    current_time = min_time
    while current_time < max_time:
        present = [
            p["name"]
            for p in players
            if to_datetime(p["start"]) <= current_time < to_datetime(p["end"])
        ]
        if present:
            cost_per_person = rate_per_min / len(present)
            for name in present:
                if name not in timeline:
                    timeline[name] = 0
                    durations[name] = 0
                timeline[name] += cost_per_person
                durations[name] += 1
        current_time += timedelta(minutes=1)

    total_cost = sum(timeline.values())

    st.markdown("## 💰 Cost Breakdown")
    for name in timeline:
        time_minutes = durations[name]
        time_hours = round(time_minutes / 60, 2)
        cost = round(timeline[name], 2)
        st.info(f"**{name}**: Played for **{time_hours}** hours | Cost: **{cost} EGP**")

    st.success(f"✅ Total Group Cost: **{round(total_cost, 2)} EGP**")
