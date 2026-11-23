import streamlit as st
import io, wave, struct, math

from agent import MineSafeAgent

st.set_page_config(page_title="MineSafe AI", page_icon="⛏️", layout="wide")

def make_alarm():
    rate = 8000
    frames = bytearray()
    for _ in range(3):
        for i in range(int(rate * 0.25)):
            v = int(20000 * math.sin(2 * math.pi * 880 * i / rate))
            frames += struct.pack("<h", v)
        frames += b"\x00\x00" * int(rate * 0.15)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))
    return buf.getvalue()







st.markdown("""
<style>
.stApp { background-color: #0b1120; color: #ffffff; }
[data-testid="stMetric"] {
    background-color: #1e293b; padding: 20px;
    border-radius: 15px; border: 1px solid #334155;
}
[data-testid="stMetricLabel"] { color: #ffffff !important; }
[data-testid="stMetricValue"] { color: #00e5a0 !important; font-size: 30px !important; }
h1, h2, h3 { color: #00e5a0 !important; }
p, label, li, span { color: #e2e8f0; }
[data-testid="stSidebar"] { background-color: #172033; }
[data-testid="stAlert"] { border-radius: 12px !important; }
[data-testid="stAlert"] p { color: #172033 !important; font-weight: 600 !important; }




.stButton button { background-color: #00e5a0; border: none; }
.stButton button p { color: #0b1120 !important; font-weight: 700 !important; }




</style>
""", unsafe_allow_html=True)

st.title("⛏️ MineSafe AI")
st.subheader("Mining Robot Navigation & Safety Monitoring System")
st.caption("AI-powered mining environment safety simulation")
st.divider()

# ---------- Sidebar sensors ----------
st.sidebar.title("⚙️ Sensor Controls")
gas = st.sidebar.slider("Gas Level (%)", 0, 100, 10)
temperature = st.sidebar.slider("Temperature (°C)", 0, 100, 30)
battery = st.sidebar.slider("Robot Battery (%)", 0, 100, 80)
obstacle = st.sidebar.selectbox("Obstacle Detection", ["No Obstacle", "Obstacle Detected"])
obstacle_value = 1 if obstacle == "Obstacle Detected" else 0
sound_on = st.sidebar.checkbox("🔊 Alarm sound", value=True)




# ---------- Dashboard ----------
st.subheader("📊 Mining Sensor Dashboard")
c1, c2, c3, c4 = st.columns(4)
c1.metric("💨 Gas Level", f"{gas}%")
c2.metric("🌡️ Temperature", f"{temperature} °C")
c3.metric("🔋 Battery", f"{battery}%")
c4.metric("🚧 Obstacle", "DETECTED" if obstacle_value else "CLEAR")
st.divider()

# ---------- AI agent ----------
agent = MineSafeAgent()
result = agent.analyze_environment(gas, temperature, battery, obstacle_value)

st.header("🚦 AI Safety Status")

if gas > 25 or temperature > 45:
    st.markdown("""
    <style>
    @keyframes flash { 0%,100% {opacity:1;} 50% {opacity:0.2;} }
    .alarm {
        background:#ff1f3d; color:white; padding:20px; border-radius:12px;
        font-size:22px; font-weight:800; text-align:center;
        animation: flash 0.8s infinite;
    }
    </style>
    <div class="alarm">🚨 DANGER: Hazardous conditions detected! EVACUATE 🚨</div>
    """, unsafe_allow_html=True)
    if sound_on:
        st.audio(make_alarm(), format="audio/wav", autoplay=True)
elif obstacle_value == 1:








    st.warning("WARNING: Obstacle detected in navigation path.")
elif battery < 20:
    st.warning("WARNING: Robot battery is low.")
else:
    st.success("SAFE: Environment appears normal in this simulation.")

st.subheader("🤖 AI Agent Analysis")
for alert in result["alerts"]:
    st.write(alert)

st.subheader("Recommended Action")
st.info(result["action"])
st.divider()

# ---------- Robot navigation ----------
st.subheader("🗺️ Interactive Robot Navigation")

# Safe path the robot follows (row, column)
PATH = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)]

BASE_MAP = [
    ["🟩", "🟩", "🟩", "🟨", "🟩", "🟩"],
    ["🟩", "🟩", "🟩", "🟩", "🟥", "🟩"],
    ["🟩", "🟩", "🟨", "🟩", "🟥", "🟩"],
    ["🟩", "🟥", "🟩", "🟩", "🟩", "🟩"],
    ["🟩", "🟩", "🟩", "🟩", "🟩", "🏁"],
]

if "step" not in st.session_state:
    st.session_state.step = 0

b1, b2 = st.columns(2)

with b1:
    if st.button("▶️ Move Robot Forward"):
        if gas > 25 or temperature > 45 or obstacle_value == 1:
            st.error("Navigation blocked due to simulated hazard.")
        elif battery < 5:
            st.error("Battery too low to move.")
        elif st.session_state.step < len(PATH) - 1:
            st.session_state.step += 1
        else:
            st.success("Destination reached! 🏁")

with b2:
    if st.button("🔄 Reset Robot"):
        st.session_state.step = 0

# Draw map with robot at current position
grid = [row[:] for row in BASE_MAP]
r, c = PATH[st.session_state.step]
grid[r][c] = "🤖"

st.markdown("### Mining Tunnel Map")
for row in grid:
    st.markdown("　".join(row))

st.markdown("""
**Map Legend**  
🟩 Safe Path  🟥 Hazard Zone  🟨 Obstacle  🤖 Robot  🏁 Destination
""")
st.divider()

# ---------- Safety rules ----------
st.header("📋 Mining Safety Rules")
rules = [
    "Monitor environmental conditions continuously.",
    "Stop operation when hazardous conditions are detected.",
    "Avoid obstacles in the navigation path.",
    "Monitor robot battery status.",
    "Report hazards through communication systems.",
    "Follow approved mining safety procedures.",
]
for rule in rules:
    st.markdown(f"✔️ {rule}")

st.divider()
st.caption("This application is a simulation and is not connected to real mining equipment.")