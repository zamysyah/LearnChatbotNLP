
import streamlit as st
import time
from chatbot import get_response

st.set_page_config(page_title="Chatbot Sederhana", layout="centered")
st.title("🤖 Chatbot Cerdas Cuaca & Canda")

# Inisialisasi sesi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input dari pengguna
user_input = st.text_input("Kamu:", "")

if user_input:
    # Tampilkan input pengguna di history
    st.session_state.chat_history.append(("Kamu", user_input))

    # Simulasi bot sedang mengetik
    with st.spinner("Bot sedang mengetik..."):
        time.sleep(1.2)
        response = get_response(user_input)
    
    st.session_state.chat_history.append(("Bot", response))

# Tampilkan semua percakapan
st.markdown("---")
st.subheader("💬 Riwayat Percakapan")

for sender, msg in st.session_state.chat_history:
    if sender == "Kamu":
        st.markdown(f"**🧑 Kamu:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
