import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="מחולל התפלגות נורמלית - קלמט", layout="centered")

st.title("📊 מחולל עקומת התפלגות נורמלית")
st.write("בחר את סוג השטח והזן ערכי Z")

# בחירת סוג החישוב
mode = st.radio(
    "מה ברצונך לחשב?",
    ("שטח משמאל (Z < x)", "שטח מימין (Z > x)", "שטח בין שני ערכים")
)

# הגדרת ערכי ה-Z בהתאם לבחירה
if mode == "שטח בין שני ערכים":
    col1, col2 = st.columns(2)
    with col1:
        z_low = st.number_input("ערך Z תחתון:", value=-1.0, step=0.01)
    with col2:
        z_high = st.number_input("ערך Z עליון:", value=1.0, step=0.01)
    if z_low > z_high:
        st.error("שים לב: הערך התחתון חייב להיות קטן מהערך העליון.")
else:
    z_score = st.number_input("הזן ערך Z:", value=0.0, step=0.01)

# לוגיקת חישוב וציור
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x, 0, 1)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y, color='blue', lw=2)

if mode == "שטח משמאל (Z < x)":
    prob = norm.cdf(z_score)
    x_fill = np.linspace(-4, z_score, 1000)
    ax.fill_between(x_fill, norm.pdf(x_fill, 0, 1), color='skyblue', alpha=0.5)
    ax.axvline(z_score, color='red', linestyle='--')
    title_text = f"Φ({z_score}) = {prob:.4f} ({prob*100:.1f}%)"

elif mode == "שטח מימין (Z > x)":
    prob = 1 - norm.cdf(z_score)
    x_fill = np.linspace(z_score, 4, 1000)
    ax.fill_between(x_fill, norm.pdf(x_fill, 0, 1), color='orange', alpha=0.5)
    ax.axvline(z_score, color='red', linestyle='--')
    title_text = f"P(Z > {z_score}) = {prob:.4f} ({prob*100:.1f}%)"

else: # שטח בין שני ערכים
    prob = norm.cdf(z_high) - norm.cdf(z_low)
    x_fill = np.linspace(z_low, z_high, 1000)
    ax.fill_between(x_fill, norm.pdf(x_fill, 0, 1), color='lightgreen', alpha=0.5)
    ax.axvline(z_low, color='green', linestyle='--')
    ax.axvline(z_high, color='green', linestyle='--')
    title_text = f"P({z_low} < Z < {z_high}) = {prob:.4f} ({prob*100:.1f}%)"

# עיצוב הגרף
ax.set_title(title_text, fontsize=14)
ax.grid(axis='y', alpha=0.2)
st.pyplot(fig)

# כפתור הורדה
plt.savefig("distribution.png")
with open("distribution.png", "rb") as file:
    st.download_button("הורד תמונה", file, "distribution.png", "image/png")