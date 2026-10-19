import json
import os
import random
from datetime import datetime
import requests
import streamlit as st

# ==========================================
# 1. НАЛАШТУВАННЯ СТОРІНКИ ТА СКЕТЧ-ДИЗАЙНУ (CSS)
# ==========================================
st.set_page_config(
    page_title="RudaFox - Крафтовий Навчальний Хаб 8 Клас",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Крафтовий папір, затишні кольори та рукописні шрифти з Google Fonts
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Comfortaa:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Comfortaa', cursive, sans-serif;
        background-color: #F5EBE0 !important;
        color: #4A3525;
    }

    .stApp {
        background: #F5EBE0;
        background-image: radial-gradient(#E6D5C3 1px, transparent 0);
        background-size: 24px 24px;
    }

    h1, h2, h3, h4 {
        font-family: 'Caveat', cursive !important;
        color: #3E2723 !important;
        font-weight: 700 !important;
    }

    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }

    /* Картки у скетч-стилі */
    .craft-card {
        background-color: #FFFDF9;
        border: 2px dashed #B08968;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 0px #DDB892;
    }

    .quote-craft {
        background-color: #FFF3E0;
        border: 2px solid #E07A5F;
        border-radius: 14px;
        padding: 16px 20px;
        font-family: 'Caveat', cursive;
        font-size: 1.5rem;
        color: #5C3D2E;
        box-shadow: 3px 3px 0px #E07A5F;
        margin-bottom: 20px;
    }

    .badge-status {
        padding: 6px 14px;
        border-radius: 12px;
        font-family: 'Comfortaa', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .status-planned { background-color: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }
    .status-process { background-color: #FFF8E1; color: #E65100; border: 1px solid #FFE082; }
    .status-done { background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
    .status-debt { background-color: #FFEBEE; color: #C62828; border: 1px solid #EF9A9A; }

    /* Кнопки у дудл-стилі */
    .stButton>button {
        border-radius: 12px !important;
        border: 2px solid #4A3525 !important;
        background-color: #81B29A !important;
        color: #FFFFFF !important;
        font-family: 'Comfortaa', sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 3px 3px 0px #4A3525 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0px #4A3525 !important;
        background-color: #6B8E23 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. БАЗА ДАНИХ ТА НАЛАШТУВАННЯ
# ==========================================
DATA_FILE = "tasks_db.json"
CONFIG_FILE = "config.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "subject": "Алгебра",
        "title": "Раціональні вирази та дроби",
        "desc": "Переглянути конспект у NotebookLM та розв'язати вправи №1-5",
        "status": "В процесі",
        "link": "https://gemini.google.com/notebook/81ad84a5-0616-4065-a9f3-a2c6c9ab6096",
        "date": "2026-10-19",
        "aspects": ["Концепції", "Логіка"],
    },
    {
        "id": 2,
        "subject": "Історія України",
        "title": "Козацько-селянські повстання 20-30-х рр. XVII ст.",
        "desc": "Опрацювати Параграф 8 підручника та переглянути флеш-картки",
        "status": "Заплановано",
        "link": "https://notebooklm.google.com/notebook/cda44234-a2b8-4615-ac33-3429b324cc5d",
        "date": "2026-10-20",import json
import os
import random
from datetime import datetime
import requests
import streamlit as st

# ==========================================
# 1. НАЛАШТУВАННЯ СТОРІНКИ ТА СКЕТЧ-ДИЗАЙНУ (CSS)
# ==========================================
st.set_page_config(
    page_title="RudaFox - Навчальний Хаб 9 Клас",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Comfortaa:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Comfortaa', cursive, sans-serif;
        background-color: #F5EBE0 !important;
        color: #4A3525;
    }

    .stApp {
        background: #F5EBE0;
        background-image: radial-gradient(#E6D5C3 1px, transparent 0);
        background-size: 24px 24px;
    }

    h1, h2, h3, h4 {
        font-family: 'Caveat', cursive !important;
        color: #3E2723 !important;
        font-weight: 700 !important;
    }

    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }

    .craft-card {
        background-color: #FFFDF9;
        border: 2px dashed #B08968;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 0px #DDB892;
    }

    .quote-craft {
        background-color: #FFF3E0;
        border: 2px solid #E07A5F;
        border-radius: 14px;
        padding: 16px 20px;
        font-family: 'Caveat', cursive;
        font-size: 1.5rem;
        color: #5C3D2E;
        box-shadow: 3px 3px 0px #E07A5F;
        margin-bottom: 20px;
    }

    .badge-status {
        padding: 6px 14px;
        border-radius: 12px;
        font-family: 'Comfortaa', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .status-planned { background-color: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }
    .status-process { background-color: #FFF8E1; color: #E65100; border: 1px solid #FFE082; }
    .status-done { background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
    .status-debt { background-color: #FFEBEE; color: #C62828; border: 1px solid #EF9A9A; }

    .stButton>button {
        border-radius: 12px !important;
        border: 2px solid #4A3525 !important;
        background-color: #81B29A !important;
        color: #FFFFFF !important;
        font-family: 'Comfortaa', sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 3px 3px 0px #4A3525 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0px #4A3525 !important;
        background-color: #6B8E23 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. БАЗА ДАНИХ ТА НАЛАШТУВАННЯ
# ==========================================
DATA_FILE = "tasks_db.json"
CONFIG_FILE = "config.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "subject": "Географія",
        "title": "Чинники розміщення виробництв",
        "desc": "Опрацювати матеріали уроку та пройти підсумковий тест.",
        "status": "В процесі",
        "link": "https://notebooklm.google.com/notebook/3eb94634-62b1-4c57-8d6b-fe3bb2343692",
        "date": "2026-10-19",
        "aspects": ["Концепції", "Термінологія"],
        "mode": "Контрольний",
        "quiz": {
            "question": "Який чинник є вирішальним для розміщення підприємств важкого машинобудування?",
            "options": ["Сировинний та споживчий", "Трудовий", "Водний"],
            "answer": "Сировинний та споживчий",
            "hint": "Важке машинобудування потребує багато металу!",
            "explanation": "Важке машинобудування орієнтується на метал (сировину) та споживача.",
        },
    },
    {
        "id": 2,
        "subject": "Всесвітня історія",
        "title": "Промисловий переворот та формування індустріального суспільства",
        "desc": "Прочитати Параграф підручника 9 класу та виконати завдання.",
        "status": "Заплановано",
        "link": "https://gemini.google.com/notebook/9c229291-3cb0-4210-a17c-12126891be8a",
        "date": "2026-10-20",
        "aspects": ["Дати та Події"],
        "mode": "Тренувальний",
        "quiz": {
            "question": "Яка країна стала 'майстернею світу' під час промислового перевороту?",
            "options": ["Франція", "Велика Британія", "США"],
            "answer": "Велика Британія",
            "hint": "Батьківщина парового двигуна.",
            "explanation": "Велика Британія першою здійснить промисловий переворот.",
        },
    },
]

MOTIVATIONAL_QUOTES = [
    "«Майбутнє належить тим, хто вірить у красу своїх мрій.» — Кішка Васька стежить за твоїм прогресом! 🐾",
    "«Лайфхак для 9-класника: 25 хвилин фокусу = вільний вечір без боргів!» 🎮⚡",
    "«Помилка — це просто інструкція, як зробити краще з другого разу!» 💡",
    "«Кішка Васька каже: закривай квест зараз, щоб увечері мати час для відпочинку!» 🐱✨",
]


def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if "tasks" not in st.session_state:
    st.session_state.tasks = load_data(DATA_FILE, DEFAULT_TASKS)

if "config" not in st.session_state:
    st.session_state.config = load_data(
        CONFIG_FILE, {"bot_token": "", "chat_id": ""}
    )


def send_telegram_msg(text):
    token = st.session_state.config.get("bot_token")
    chat_id = st.session_state.config.get("chat_id")
    if not token or not chat_id:
        return (
            False,
            "⚠️ Вкажіть Telegram Bot Token та Chat ID у Кабінеті мами!",
        )
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(
            url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )
        if res.status_code == 200:
            return True, "🚀 Сповіщення успішно надіслано в Телеграм!"
        else:
            return False, f"Помилка Telegram API: {res.text}"
    except Exception as e:
        return False, f"Помилка з'єднання: {e}"


# ==========================================
# 3. БІЧНА ПАНЕЛЬ
# ==========================================
st.sidebar.markdown("# 🦊 RudaFox Hub")
st.sidebar.caption("🎓 Навчальний простір 9 класу")

role = st.sidebar.radio(
    "📍 Оберіть кабінет:",
    ["👦 Кабінет Івана (Учень)", "👩‍🏫 Кабінет мами (Конструктор & Налаштування)"],
)

SUBJECTS = [
    "Усі предмети",
    "Алгебра",
    "Геометрія",
    "Фізика",
    "Хімія",
    "Біологія",
    "Географія",
    "Правознавство",
    "Історія України",
    "Всесвітня історія",
    "Українська література",
    "Зарубіжна література",
    "English",
    "Інформатика",
]

# ==========================================
# 4. КАБІНЕТ ІВАНА
# ==========================================
if role == "👦 Кабінет Івана (Учень)":
    st.title("📜 Щоденник навчальних квестів Івана — 9 Клас")

    st.markdown(
        f'<div class="quote-craft">💬 <b>Порада від кішки Васьки:</b><br>{random.choice(MOTIVATIONAL_QUOTES)}</div>',
        unsafe_allow_html=True,
    )

    debts_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Борг"
    )
    done_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Виконано"
    )
    total_count = len(st.session_state.tasks)

    col1, col2, col3 = st.columns(3)
    col1.metric("Уроки на сьогодні", total_count)
    col2.metric("Завершено ✅", done_count)
    col3.metric("Хвости 🚨", debts_count)

    st.markdown("---")
    selected_subject = st.selectbox("🔍 Фільтр за предметом:", SUBJECTS)

    filtered = st.session_state.tasks
    if selected_subject != "Усі предмети":
        filtered = [t for t in filtered if t["subject"] == selected_subject]

    st.subheader("📚 Твої квести та уроки")

    if not filtered:
        st.info("У цій категорії поки немає завдань.")

    for task in filtered:
        st.markdown('<div class="craft-card">', unsafe_allow_html=True)
        col_a, col_b = st.columns([3, 1])

        with col_a:
            status_cls = {
                "Заплановано": "status-planned",
                "В процесі": "status-process",
                "Виконано": "status-done",
                "Борг": "status-debt",
            }.get(task["status"], "")

            st.markdown(
                f"### {task['subject']}: {task['title']} <span class='badge-status {status_cls}'>{task['status']}</span>",
                unsafe_allow_html=True,
            )
            st.write(f"📝 **Завдання:** {task['desc']}")

            if task.get("link"):
                st.markdown(f"🔗 [Перейти до матеріалів]({task['link']})")

            # Блок проходження тесту
            score_text = "100% (1/1)"
            if task.get("quiz"):
                with st.expander("🧩 Пройти інтерактивний тест"):
                    q = task["quiz"]
                    u_ans = st.radio(
                        q["question"], q["options"], key=f"q_ans_{task['id']}"
                    )

                    col_q1, col_q2 = st.columns(2)
                    with col_q1:
                        if st.button("💡 Підказка", key=f"btn_hint_{task['id']}"):
                            st.info(f"🔑 {q.get('hint', 'Підказка відсутня')}")
                    with col_q2:
                        if st.button(
                            "Перевірити відповідь", key=f"btn_chk_{task['id']}"
                        ):
                            if u_ans == q["answer"]:
                                st.success("✨ Абсолютно вірно!")
                                score_text = "100% (1/1)"
                            else:
                                st.error("❌ Помилка!")
                                st.warning(
                                    f"💡 Пояснення: {q.get('explanation', '')}"
                                )
                                score_text = "0% (0/1)"

        with col_b:
            st.write("**Здача уроку:**")
            mode_str = task.get("mode", "Контрольний")
            st.caption(f"⚙️ Режим: **{mode_str}**")

            if task["status"] != "Виконано":
                if st.button(
                    "✅ Завершити урок", key=f"finish_btn_{task['id']}"
                ):
                    task["status"] = "Виконано"
                    save_data(DATA_FILE, st.session_state.tasks)

                    # Розрахунок статистики для кастомного звіту
                    new_done_count = sum(
                        1
                        for t in st.session_state.tasks
                        if t["status"] == "Виконано"
                    )
                    daily_pct = int(
                        (
                            new_done_count
                            / max(len(st.session_state.tasks), 1)
                        )
                        * 100
                    )
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # ФОРМУВАННЯ КАСКАДНОГО ЗВІТУ ЗІ СКРІНШОТА
                    tg_report = (
                        f"🦊 **ЗВІТ З МІСЦЯ СТРАЖДАНЬ ТА ДОСЯГНЕНЬ**\n\n"
                        f"📚 **Предмет:** {task['subject']}\n"
                        f"📖 **Тема:** {task['title']}\n"
                        f"🏋️‍♂️ **Режим:** {mode_str}\n"
                        f"📊 **Результат тесту:** {score_text}\n"
                        f"📈 **Прогрес за день:** {new_done_count} з {len(st.session_state.tasks)} уроків закрито ({daily_pct}%)\n"
                        f"⏰ **Час здачі:** {now_str}\n\n"
                        f"*Кішка Васька задоволено мурчить та оцінює успіхи! 🐾✨*"
                    )

                    st.balloons()
                    send_telegram_msg(tg_report)
                    st.success("🎉 Звіт автоматично відправлено в Телеграм!")
                    st.rerun()
            else:
                st.success("Урок закрито! ✅")

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. КАБІНЕТ МАМИ
# ==========================================
else:
    st.title("👩‍🏫 Кабінет мами — «Місце сили RudaFox (9 Клас)»")

    tab_create, tab_manage, tab_telegram = st.tabs(
        [
            "🛠️ Конструктор нового уроку",
            "📋 Управління уроками",
            "📲 Налаштування Telegram",
        ]
    )

    with tab_create:
        st.subheader("➕ Створити новий урок для 9 класу")

        with st.form("full_lesson_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                subj = st.selectbox("Предмет:", SUBJECTS[1:])
                t_title = st.text_input("Назва теми / уроку:")
                t_date = st.date_input(
                    "Дата виконання:", datetime.today()
                ).strftime("%Y-%m-%d")
            with col_f2:
                t_link = st.text_input("Посилання на матеріали (NotebookLM):")
                t_mode = st.selectbox(
                    "Режим тестування:", ["Контрольний", "Тренувальний"]
                )
                t_status = st.selectbox(
                    "Початковий статус:",
                    ["Заплановано", "В процесі", "Борг", "Виконано"],
                )

            t_desc = st.text_area("Опис завдання для Івана:")

            st.markdown("---")
            st.markdown("### 🧩 Інтерактивний тест для уроку")
            q_text = st.text_input("Запитання:")
            q_opt1 = st.text_input("Варіант 1 (Правильний):")
            q_opt2 = st.text_input("Варіант 2:")
            q_opt3 = st.text_input("Варіант 3:")
            q_hint = st.text_input("💡 Підказка:")
            q_exp = st.text_area("💡 Пояснення відповіді:")

            btn_save = st.form_submit_button("💾 Зберегти урок")

            if btn_save and t_title:
                new_id = (
                    max([t["id"] for t in st.session_state.tasks], default=0)
                    + 1
                )
                quiz_obj = None
                if q_text and q_opt1 and q_opt2:
                    opts = [q_opt1, q_opt2]
                    if q_opt3:
                        opts.append(q_opt3)
                    quiz_obj = {
                        "question": q_text,
                        "options": sorted(opts),
                        "answer": q_opt1,
                        "hint": q_hint,
                        "explanation": q_exp,
                    }

                new_task = {
                    "id": new_id,
                    "subject": subj,
                    "title": t_title,
                    "desc": t_desc,
                    "status": t_status,
                    "link": t_link,
                    "mode": t_mode,
                    "date": t_date,
                    "quiz": quiz_obj,
                }
                st.session_state.tasks.append(new_task)
                save_data(DATA_FILE, st.session_state.tasks)
                st.success(f"✨ Урок '{t_title}' додано!")
                st.rerun()

    with tab_manage:
        st.subheader("📋 Списки уроків")
        for idx, task in enumerate(st.session_state.tasks):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 1])
            col_m1.write(f"**[{task['subject']}]** {task['title']}")
            col_m2.caption(f"Статус: {task['status']} | Режим: {task.get('mode', 'Контрольний')}")
            if col_m3.button("🗑️ Видалити", key=f"del_task_{task['id']}"):
                st.session_state.tasks.pop(idx)
                save_data(DATA_FILE, st.session_state.tasks)
                st.rerun()

    with tab_telegram:
        st.subheader("⚙️ Telegram Налаштування")
        with st.form("tg_form"):
            t_token = st.text_input(
                "Bot Token:",
                value=st.session_state.config.get("bot_token", ""),
                type="password",
            )
            t_chat = st.text_input(
                "Chat ID:", value=st.session_state.config.get("chat_id", "")
            )
            if st.form_submit_button("💾 Зберегти"):
                st.session_state.config["bot_token"] = t_token
                st.session_state.config["chat_id"] = t_chat
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Збережено!")
