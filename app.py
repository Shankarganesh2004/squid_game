import streamlit as st
import random
from PIL import Image
import pygame

# ✅ Page config
st.set_page_config(page_title="Squid Game - Red Light, Green Light", layout="centered")
st.title("🦑 Squid Game: Red Light, Green Light")
st.subheader("Multiplayer Version (Python + Streamlit)")

# ✅ Init mixer for sounds
try:
    pygame.mixer.init()
except:
    st.warning("⚠️ Pygame mixer failed to initialize (may not work in browser mode).")

# ✅ Sound function
def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except:
        st.error(f"❌ Couldn't play: {sound_file}")

# ✅ Session state setup
if 'players' not in st.session_state:
    st.session_state.players = {}
if 'light' not in st.session_state:
    st.session_state.light = 'green'
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

# ✅ Game setup (before start)
if not st.session_state.game_started:
    st.info("👆 Choose number of players and press 'Start Game' to begin!")
    num_players = st.slider("Select number of players", 2, 4, 2)
    player_names = []

    for i in range(num_players):
        name = st.text_input(f"Player {i+1} name", f"Player{i+1}")
        player_names.append(name)

    if st.button("🚦 Start Game"):
        st.session_state.players = {name: {"position": 0, "status": "alive"} for name in player_names}
        st.session_state.game_started = True
        # ❌ No experimental_rerun needed — Streamlit auto-refreshes state
        st.success("✅ Game Started! Scroll down to play.")
else:
    # ✅ Show current light
    light_img = "assets/green_light.png" if st.session_state.light == 'green' else "assets/red_light.png"
    st.image(Image.open(light_img), width=100)
    st.markdown(f"### Current Light: :{'green_circle:' if st.session_state.light == 'green' else 'red_circle:'} **{st.session_state.light.upper()}**")

    # ✅ Light switch
    if st.button("🔁 Switch Light"):
        st.session_state.light = 'green' if random.random() > 0.5 else 'red'
        play_sound("assets/background.mp3")

    # ✅ Player movement and progress
    for player in st.session_state.players:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.session_state.players[player]['status'] == "alive":
                st.progress(st.session_state.players[player]['position'] / 100)
            else:
                st.markdown(f"☠️ **{player} Eliminated**")
        with col2:
            if st.session_state.players[player]['status'] == "alive":
                if st.button(f"🚶 Move ({player})"):
                    if st.session_state.light == 'red':
                        st.session_state.players[player]['status'] = "eliminated"
                        play_sound("assets/eliminated.mp3")
                    else:
                        st.session_state.players[player]['position'] += random.randint(5, 15)
                        if st.session_state.players[player]['position'] >= 100:
                            st.session_state.winner = player
                            play_sound("assets/success.mp3")
                            st.session_state.game_started = False
                            st.balloons()
                            break

    # ✅ Declare winner
    if st.session_state.winner:
        st.success(f"🎉 {st.session_state.winner} wins the game!")
        if st.button("🔄 Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
