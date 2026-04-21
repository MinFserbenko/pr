import streamlit as st
import json
from pathlib import Path

st.set_page_config(layout="wide")

DATA_FILE = "coffee_state.json"

# =======================
# STYLE (как твой Tkinter)
# =======================
st.markdown("""
<style>
body {
    background-color: #2A2018;
    color: #E8DCC8;
}
.block-container {
    padding-top: 1rem;
}
.card {
    background-color: #4E3A2C;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# DATA
# =======================
def load():
    if not Path(DATA_FILE).exists():
        return {"recipes": [], "favorites": []}
    return json.loads(Path(DATA_FILE).read_text(encoding="utf-8"))

def save(data):
    Path(DATA_FILE).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

if "data" not in st.session_state:
    st.session_state.data = load()

if "selected" not in st.session_state:
    st.session_state.selected = None

if "fav_mode" not in st.session_state:
    st.session_state.fav_mode = False

# =======================
# LAYOUT
# =======================
left, right = st.columns([1, 3])

# =======================
# LEFT PANEL (ФИЛЬТРЫ)
# =======================
with left:
    st.markdown("## ФИЛЬТРЫ")

    eq = st.selectbox("Оборудование", ["Все","Эспрессо-машина","Турка","Пуровер V60","Хемекс","Шейкер"])
    flavor = st.selectbox("Вкус", ["Любой","Кислый","Сладкий","Горький"])
    milk = st.selectbox("Молоко", ["Не важно","С молоком","Без молока"])
    comp = st.selectbox("Сложность", ["Любая","Лёгкая","Средняя"])

    if st.button("Найти"):
        pass

    if st.button("Избранное"):
        st.session_state.fav_mode = not st.session_state.fav_mode

    st.markdown("---")

    # ДОБАВЛЕНИЕ РЕЦЕПТА
    with st.expander("➕ Добавить рецепт"):
        name = st.text_input("Название")
        desc = st.text_input("Описание")
        time = st.text_input("Время")
        cal = st.text_input("Калории")

        equipment = st.selectbox("Оборудование", ["Эспрессо-машина","Турка","Шейкер"])
        fl = st.selectbox("Вкус", ["Кислый","Сладкий","Горький"])
        ml = st.selectbox("Молоко", ["С молоком","Без молока"])
        cp = st.selectbox("Сложность", ["Лёгкая","Средняя"])

        det = st.text_area("Рецепт")

        if st.button("Сохранить рецепт"):
            st.session_state.data["recipes"].append({
                "name": name,
                "equipment": equipment,
                "flavor": fl,
                "milk": ml,
                "complexity": cp,
                "description": desc,
                "time_minutes": time,
                "calories": cal,
                "details": det,
            })
            save(st.session_state.data)
            st.success("Сохранено")

# =======================
# FILTER LOGIC
# =======================
def ok(r):
    if st.session_state.fav_mode and r["name"] not in st.session_state.data["favorites"]:
        return False
    if eq != "Все" and r["equipment"] != eq:
        return False
    if flavor != "Любой" and r["flavor"] != flavor:
        return False
    if milk != "Не важно" and r["milk"] != milk:
        return False
    if comp != "Любая" and r["complexity"] != comp:
        return False
    return True

recipes = [r for r in st.session_state.data["recipes"] if ok(r)]

# =======================
# RIGHT PANEL
# =======================
with right:
    st.markdown("## РЕЦЕПТЫ")

    for r in recipes:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(("⭐ " if r["name"] in st.session_state.data["favorites"] else "") + r["name"])
        st.caption(r["description"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Показать", key=r["name"]):
                st.session_state.selected = r

        with col2:
            favs = st.session_state.data["favorites"]
            if r["name"] in favs:
                if st.button("Убрать", key="rm"+r["name"]):
                    favs.remove(r["name"])
                    save(st.session_state.data)
            else:
                if st.button("В избранное", key="add"+r["name"]):
                    favs.append(r["name"])
                    save(st.session_state.data)

        st.markdown('</div>', unsafe_allow_html=True)

# =======================
# BOTTOM PANEL (как у тебя)
# =======================
st.markdown("---")
st.markdown("## РЕЦЕПТ")

if st.session_state.selected:
    st.text_area("", st.session_state.selected["details"], height=300)
else:
    st.info("Выбери рецепт")
