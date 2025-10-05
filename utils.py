import ast

def parse_nutrition(nutrition_str):
    """
    Mengubah kolom 'nutrition' dari string menjadi dictionary label gizi.
    Format dataset Food.com: [calories, fat, sugar, sodium, protein, sat_fat, carbs]
    """
    try:
        values = ast.literal_eval(nutrition_str)
        labels = [
            "Kalori (kcal)",
            "Lemak (g)",
            "Gula (g)",
            "Sodium (mg)",
            "Protein (g)",
            "Lemak Jenuh (g)",
            "Karbohidrat (g)"
        ]
        return {labels[i]: round(values[i], 2) for i in range(len(values))}
    except Exception:
        return {}

def clean_ingredients(ingredients_str):
    """Ubah list bahan jadi string mudah dibaca."""
    try:
        ingredients = ast.literal_eval(ingredients_str)
        return ", ".join(ingredients)
    except Exception:
        return ingredients_str

def format_steps(steps_str):
    """Ubah list langkah jadi bullet list."""
    try:
        steps = ast.literal_eval(steps_str)
        return "\n".join([f"• {step}" for step in steps])
    except Exception:
        return steps_str

