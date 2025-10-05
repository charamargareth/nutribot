import streamlit as st
from app.backend import get_recipes_by_ingredient, analyze_nutrition, ask_ai
from app.utils import clean_ingredients

st.set_page_config(page_title="NutriBot", layout="wide")
st.title("NutriBot – AI Food & Nutrition Chatbot")
st.caption("Tanyakan resep, analisis gizi, atau saran makanan sehat!")

# Sidebar konfigurasi
st.sidebar.header("⚙️ Pengaturan Chatbot")
tone = st.sidebar.radio("Gaya Bahasa:", ["Santai", "Formal"])
limit = st.sidebar.slider("Jumlah Rekomendasi Resep:", 1, 5, 3)

# Simpan riwayat chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ketik pertanyaanmu di sini:")

if st.button("Kirim"):
    if user_input:
        with st.spinner("Sedang mencari jawaban..."):
            # Deteksi apakah user menyebut bahan makanan
            keywords = ["ayam", "ikan", "sayur", "telur", "tahu", "tempe", "nasi", "daging", "roti", "mie"]
            if any(word in user_input.lower() for word in keywords):
                recipes = get_recipes_by_ingredient(user_input, limit)
                if not recipes.empty:
                    response = "Berikut beberapa resep yang cocok:\n\n"
                    for _, row in recipes.iterrows():
                        nutr = analyze_nutrition(row["nutrition"])
                        response += f"🍴 **{row['name']}**\n"
                        response += f"- Kalori: {nutr.get('Kalori (kcal)', '-')} kcal | Protein: {nutr.get('Protein (g)', '-')} g | Lemak: {nutr.get('Lemak (g)', '-')} g\n"
                        response += f"- Bahan: {clean_ingredients(row['ingredients'])[:120]}...\n\n"
                else:
                    response = "Maaf, aku tidak menemukan resep yang cocok 😔."
            else:
                response = ask_ai(user_input, tone)
            
            st.session_state.chat_history.append((user_input, response))

# Tampilkan riwayat chat
st.subheader("Riwayat Chat")
for chat in st.session_state.chat_history[::-1]:
    st.markdown(f"👩‍💻 **Kamu:** {chat[0]}")
    st.markdown(f"🤖 **NutriBot:** {chat[1]}")
