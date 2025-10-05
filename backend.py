import os
import pandas as pd
import openai
from dotenv import load_dotenv
from utils import parse_nutrition, clean_ingredients, format_steps

# Load API Key dari file .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === LOAD DATASET ===
DATA_PATH = "data/RAW_recipes.csv"
recipes_df = pd.read_csv(DATA_PATH)
recipes_df = recipes_df[['name', 'ingredients', 'nutrition', 'steps']].dropna()

def get_recipes_by_ingredient(ingredient, limit=3):
    """Cari resep berdasarkan bahan makanan."""
    result = recipes_df[recipes_df['ingredients'].str.contains(ingredient, case=False, na=False)]
    return result.head(limit)

def analyze_nutrition(nutrition_str):
    """Parsing nutrisi pakai fungsi dari utils."""
    return parse_nutrition(nutrition_str)

def ask_ai(prompt, tone="Santai"):
    """Gunakan GPT untuk menjawab pertanyaan umum tentang makanan/gizi."""
    style = "Gunakan bahasa santai dan ramah" if tone.lower() == "santai" else "Gunakan bahasa formal dan sopan"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Kamu adalah asisten gizi yang ramah dan informatif. {style}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]