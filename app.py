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
        "date": "2026-10-20",
        "aspects": ["Дати", "Критичне мислення"],
    },
    {
        "id": 3,
        "subject": "Фізика",
        "title": "Теплові явища та температура",
        "desc": "Записати формулу кількості теплоти та прослухати подкаст",
        "status": "Борг",
        "link": "https://gemini.google.com/notebook/7793e49a-6df1-4fbc-a25b-a2ae9145c112",
        "date": "2026-10-18",
        "aspects": ["Формули", "Практика"],
    },
]

MOTIVATIONAL_QUOTES = [
    "«Майбутнє належить тим, хто вірить у красу своїх мрій.» — Кунг-фу Панда 🐼",
    "«Навіть найдовша дорога починається з першого кроку.» — Хоббіт 🧙‍♂️",
    "«Ти сміливіший, ніж віриш, сильніший, ніж здаєшся, і розумніший, ніж думаєш!» — Вінні Пух 🍯",
    "«Лайфхак для підлітка: 25 хвилин фокусу на фізиці = +2 години для ігор увечері без докорів сумління!» 🎮⚡",
    "«Помилка — це не поразка, це просто інструкція, як зробити краще з другого разу!» 💡",
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
        return False, "Будь ласка, вкажіть Bot Token та Chat ID у Кабінеті мами!"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(
            url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )
        if res.status_code == 200:
            return True, "Звіт успішно надіслано в Телеграм!"
        else:
            return False, f"Помилка Телеграм API: {res.text}"
    except Exception as e:
        return False, f"Помилка з'єднання: {e}"


# ==========================================
# 3. БІЧНА ПАНЕЛЬ (НАВІГАЦІЯ)
# ==========================================
st.sidebar.markdown("# 🦊 RudaFox Hub")
st.sidebar.caption("Затишний навчальний простір 8 класу")

menu = st.sidebar.radio(
    "📍 Навігація:",
    [
        "👦 Кабінет Івана",
        "🧩 Інтерактивні Тести",
        "📘 NotebookLM & Медіа",
        "🎬 Відео-Лабораторія (Claude)",
        "👩‍🏫 Кабінет мами (Місце сили)",
    ],
)

SUBJECTS = [
    "Усі предмети",
    "Алгебра",
    "Геометрія",
    "Фізика",
    "Хімія",
    "Історія України",
    "Всесвітня історія",
    "Українська література",
    "Зарубіжна література",
    "English",
    "Інформатика",
    "Громадянська освіта",
]

# ==========================================
# 4. КАБІНЕТ ІВАНА
# ==========================================
if menu == "👦 Кабінет Івана":
    st.title("📜 Щоденник Івана — 9 Клас")

    # Мотиваційна фраза дня
    quote_today = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(
        f'<div class="quote-craft">💬 <b>Цитата / Лайфхак дня:</b><br>{quote_today}</div>',
        unsafe_allow_html=True,
    )

    debts_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Борг"
    )
    done_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Виконано"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Всього квестів", len(st.session_state.tasks))
    col2.metric("Закрито ✅", done_count)
    col3.metric("Хвости 🚨", debts_count)

    st.markdown("---")
    selected_subject = st.selectbox("🔍 Фільтр за предметом:", SUBJECTS)

    filtered = st.session_state.tasks
    if selected_subject != "Усі предмети":
        filtered = [t for t in filtered if t["subject"] == selected_subject]

    st.subheader("📌 Твої завдання на сьогодні")

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
            st.write(f"📝 {task['desc']}")
            if task.get("link"):
                st.markdown(f"🔗 [Відкрити матеріали уроку]({task['link']})")

        with col_b:
            new_st = st.selectbox(
                "Змінити статус:",
                ["Заплановано", "В процесі", "Виконано", "Борг"],
                index=["Заплановано", "В процесі", "Виконано", "Борг"].index(
                    task["status"]
                ),
                key=f"st_{task['id']}",
            )
            if new_st != task["status"]:
                task["status"] = new_st
                save_data(DATA_FILE, st.session_state.tasks)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. ІНТЕРАКТИВНІ ТЕСТИ (ТРЕНУВАЛЬНИЙ ТА КОНТРОЛЬНИЙ)
# ==========================================
elif menu == "🧩 Інтерактивні Тести":
    st.title("🧩 Конструктор та Проходження Тестів")
    st.write(
        "Оберіть режим: **Тренувальний** (із підказками та повтором) або **Контрольний** (фіксація балів)."
    )

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        test_mode = st.radio(
            "🎮 Режим тестування:",
            [
                "🏋️‍♂️ Тренувальний (з підказками)",
                "⏱️ Контрольний (оцінювання)",
            ],
        )
    with col_t2:
        num_q = st.slider("Кількість запитань у тесті:", 1, 24, 8)
        aspects = st.multiselect(
            "🎯 Аспекти для перевірки:",
            [
                "Дати та Події",
                "Концепції та Теореми",
                "Критичне мислення",
                "Логіка та Формули",
                "Практичні задачі",
                "Термінологія",
            ],
            default=["Концепції та Теореми", "Логіка та Формули"],
        )

    st.markdown("---")
    st.subheader("📚 Інтерактивний тест з Алгебри / Історії")

    sample_questions = [
        {
            "q": "Яка з наведених рівностей є тотожністю для раціональних дробів?",
            "opts": ["(a/b) * (c/d) = (ac)/(bd)", "a/b + c/d = (a+c)/(b+d)", "a/b - c/b = (a+c)/b"],
            "ans": "(a/b) * (c/d) = (ac)/(bd)",
            "hint": "Пам'ятай: при множенні дробів чисельник множиться на чисельник, а знаменник на знаменник!",
            "explanation": "Правильне правило множення раціональних дробів: чисельники та знаменники перемножуються відповідно.",
        },
        {
            "q": "У якому році відбулося повстання під проводом Тараса Трясила?",
            "opts": ["1630 рік", "1648 рік", "1625 рік"],
            "ans": "1630 рік",
            "hint": "Це повстання відбулося на початку 1630-х років і завершилося «Переяславською ніччю».",
            "explanation": "Козацьке повстання під проводом Тараса Федоровича (Трясила) відбулося у 1630 році.",
        },
    ]

    score = 0
    for idx, q in enumerate(sample_questions[:num_q]):
        st.markdown(f"**Запитання {idx + 1}: {q['q']}**")
        ans = st.radio(f"Варіант відповіді:", q["opts"], key=f"test_q_{idx}")

        if "Тренувальний" in test_mode:
            if st.button(f"💡 Отримати підказку квесту {idx + 1}", key=f"hint_{idx}"):
                st.info(f"🔑 Підказка: {q['hint']}")

            if st.button(f"Перевірити запитання {idx + 1}", key=f"check_{idx}"):
                if ans == q["ans"]:
                    st.success("✨ Абсолютно вірно!")
                else:
                    st.error(f"❌ Помилка! Пояснення: {q['explanation']}")
                    st.warning("🔄 Спробуй ще раз аналогічну картку після повторення!")
        else:
            if ans == q["ans"]:
                score += 1
        st.markdown("---")

    if "Контрольний" in test_mode:
        if st.button("🏁 Завершити контрольний тест та зберегти результат"):
            st.balloons()
            result_txt = f"📊 **Результат контрольного тесту Івана:** {score} з {min(num_q, len(sample_questions))} балів!"
            st.success(result_txt)
            send_telegram_msg(result_txt)

# ==========================================
# 6. NOTEBOOKLM ТА МЕДІА
# ==========================================
elif menu == "📘 NotebookLM & Медіа":
    st.title("📘 Інтеграція з NotebookLM & Медіа-Хаб")
    st.write(
        "Центральне сховище знань Івана: флеш-картки, подкасти, презентації та звіти."
    )

    tab1, tab2, tab3 = st.tabs(
        ["🎴 Флеш-картки", "🎧 Аудіо-Подкасти (NotebookLM)", "📊 Звіти та Конспекти"]
    )

    with tab1:
        st.subheader("Картки для швидкого запам'ятовування (Quizlet / NotebookLM)")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
            **⚡ Фізика: Теплові явища**
            - *Питання:* Яка одиниця вимірювання кількості теплоти в SI?
            - *Відповідь:* Джоуль (Дж).
            """)
        with col_c2:
            st.markdown("""
            **📜 Історія: Поняття**
            - *Питання:* Що таке 'Ординація Війська Запорозького'?
            - *Відповідь:* Документ 1638 року, що суттєво обмежував права козацтва.
            """)

    with tab2:
        st.subheader("🎧 Генеруємо Audio Overview (Подкасти за темами)")
        st.info("Ви можете прослухати аудіопояснення теми за 5 хвилин!")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

    with tab3:
        st.subheader("📝 Аналітичний звіт з теми від NotebookLM")
        st.write("Автоматично згенерований конспект за підручником 8 класу.")

# ==========================================
# 7. ВІДЕО-ЛАБОРАТОРІЯ (CLAUDE API)
# ==========================================
elif menu == "🎬 Відео-Лабораторія (Claude)":
    st.title("🎬 Генератор Сценаріїв Навчальних Відео (Claude API)")
    st.write(
        "Створення коротких відеопояснень (1-3 хв) для складних тем за допомогою ШІ."
    )

    topic = st.text_input(
        "Введіть складну тему 8 класу (наприклад: 'Дискримінант в алгебрі'):"
    )
    if st.button("🪄 Згенерувати сценарій відео з Claude"):
        if topic:
            st.subheader(f"🎬 Сценарій відеопояснення: {topic}")
            st.markdown(
                f"""
            **[00:00 - 00:30] Вступ та інтрига:**  
            *Кадр:* Гумористична анімація з кицькою Васкою.  
            *Диктор:* «Думаєш, дискримінант це складно? Насправді це просто формула-ключ, яка каже, скільки розв'язків має квадратне рівняння!»  

            **[00:30 - 01:30] Основна суть та формула:**  
            *Кадр:* Покроковий запис формули $D = b^2 - 4ac$.  
            *Диктор:* «Якщо D > 0 — маємо 2 корені. Якщо D = 0 — один. Якщо D < 0 — коренів немає!»  

            **[01:30 - 02:00] Фінальний лайфхак:**  
            *Диктор:* «Запом'ятай цей алгоритм і закривай домашку з алгебри за 5 хвилин!»
            """
            )
        else:
            st.warning("Введіть тему для генерації!")

# ==========================================
# 8. КАБІНЕТ МАМИ (МІСЦЕ СИЛИ)
# ==========================================
else:
    st.title("👩‍🏫 Кабінет мами — Налаштування RudaFox")

    st.subheader("⚙️ Налаштування Автоматичного Телеграм-Бота")
    with st.form("config_form"):
        token_input = st.text_input(
            "Telegram Bot Token:",
            value=st.session_state.config.get("bot_token", ""),
            type="password",
        )
        chat_id_input = st.text_input(
            "Telegram Chat ID (або Ваш ID):",
            value=st.session_state.config.get("chat_id", ""),
        )
        save_conf = st.form_submit_button("💾 Зберегти налаштування Телеграм")

        if save_conf:
            st.session_state.config["bot_token"] = token_input
            st.session_state.config["chat_id"] = chat_id_input
            save_data(CONFIG_FILE, st.session_state.config)
            st.success("Налаштування Телеграм успішно збережено!")

    st.markdown("---")
    st.subheader("📲 Автоматична відправка щоденного звіту")

    if st.button("🚀 Надіслати звіт про успіхи Івана в Телеграм зараз"):
        debts = [t for t in st.session_state.tasks if t["status"] == "Борг"]
        dones = [
            t for t in st.session_state.tasks if t["status"] == "Виконано"
        ]

        msg = f"🦊 **RudaFox Hub — Звіт за {datetime.now().strftime('%d.%m.%Y')}**\n\n"
        msg += f"✅ **Виконано завдань ({len(dones)}):**\n"
        for d in dones:
            msg += f" • {d['subject']}: {d['title']}\n"

        msg += f"\n🚨 **Навчальні хвости ({len(debts)}):**\n"
        if debts:
            for db in debts:
                msg += f" • {db['subject']}: {db['title']}\n"
            msg += "\n*Кіт Васька чекає виконання боргів! 🐾*"
        else:
            msg += " • Боргів немає! Ти супер-молодець! 🎉\n"

        success, res_msg = send_telegram_msg(msg)
        if success:
            st.success(res_msg)
        else:
            st.error(res_msg)
