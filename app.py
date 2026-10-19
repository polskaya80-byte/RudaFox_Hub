import json
import os
from datetime import datetime
import streamlit as st

# ==========================================
# 1. НАЛАШТУВАННЯ СТОРІНКИ ТА СТИЛІВ (CSS)
# ==========================================
st.set_page_config(
    page_title="RudaFox - Навчальний Хаб 8 Клас",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Затишні стилі у теплій колірній гамі та скетч-естетиці
st.markdown(
    """
    <style>
    .main {
        background-color: #FAFAFA;
    }
    .stAppHeader {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .card-task {
        background-color: #FFFFFF;
        border: 2px solid #EFEBE9;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
    }
    .badge-status {
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-planned { background-color: #E3F2FD; color: #1565C0; }
    .status-process { background-color: #FFF3E0; color: #E65100; }
    .status-done { background-color: #E8F5E9; color: #2E7D32; }
    .status-debt { background-color: #FFEBEE; color: #C62828; }
    
    .quote-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFB300;
        padding: 12px 18px;
        border-radius: 6px;
        font-style: italic;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. ЗБЕРЕЖЕННЯ ТА ЗАТАВАННЯ ДАНИХ (JSON)
# ==========================================
DATA_FILE = "tasks_db.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "subject": "Алгебра",
        "title": "Раціональні вирази та дроби",
        "desc": "Переглянути конспект у NotebookLM та розв'язати вправи №1-5",
        "status": "В процесі",
        "link": "https://gemini.google.com/notebook/81ad84a5-0616-4065-a9f3-a2c6c9ab6096",
        "date": "2026-10-19",
        "quiz": {
            "question": "Що таке допустимі значення змінної (ДЗЗ) для дробу a / (b - 2)?",
            "options": ["b ≠ 0", "b ≠ 2", "b ≠ -2", "Будь-які числа"],
            "answer": "b ≠ 2",
        },
    },
    {
        "id": 2,
        "subject": "Історія України",
        "title": "Козацько-селянські повстання 20-30-х рр. XVII ст.",
        "desc": "Опрацювати Параграф 8 підручника та пройти інтерактивний тест у Wordwall",
        "status": "Заплановано",
        "link": "https://notebooklm.google.com/notebook/cda44234-a2b8-4615-ac33-3429b324cc5d",
        "date": "2026-10-20",
        "quiz": None,
    },
    {
        "id": 3,
        "subject": "Фізика",
        "title": "Теплові явища та температура",
        "desc": "Записати формулу кількості теплоти та подивитися відеопояснення",
        "status": "Борг",
        "link": "https://gemini.google.com/notebook/7793e49a-6df1-4fbc-a25b-a2ae9145c112",
        "date": "2026-10-18",
        "quiz": None,
    },
]


def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_TASKS
    return DEFAULT_TASKS


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ==========================================
# 3. БІЧНА ПАНЕЛЬ (НАВІГАЦІЯ ТА РОЛІ)
# ==========================================
st.sidebar.title("🦊 RudaFox Hub")
role = st.sidebar.radio(
    "Оберіть кабінет:",
    ["👦 Кабінет учня (Іван)", "👩‍🏫 Кабінет мами (Місце сили)"],
)

st.sidebar.markdown("---")
st.sidebar.caption("🤖 **Інтегровані сервіси:**")
st.sidebar.markdown("""
- 📘 [NotebookLM](https://notebooklm.google.com)
- 🎴 [Quizlet](https://quizlet.com)
- 🎮 [Wordwall](https://wordwall.net)
- 🎨 [Canva](https://canva.com)
""")

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
# 4. КАБІНЕТ УЧНЯ (ІВАН)
# ==========================================
if role == "👦 Кабінет учня (Іван)":
    st.title("👦 Вітаю в робочому просторі, Іване!")

    # Візуальний борговий індикатор з гумором
    debts_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Борг"
    )
    done_count = sum(
        1 for t in st.session_state.tasks if t["status"] == "Виконано"
    )
    total_count = len(st.session_state.tasks)

    if debts_count == 0:
        quote = "🎉 **0 боргів!** Ти справжня легенда 8 класу. Кіт Васька пишається тобою!"
    elif debts_count <= 2:
        quote = f"😼 **У тебе {debts_count} хвости(ки).** Нічого критичного, розберемо за 20 хвилин!"
    else:
        quote = f"⚠️ **{debts_count} боргів!** Васька дивиться на тебе з докором, а мама готує чай і серйозну розмову 😉"

    st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)

    # Метрики за день
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Заплановано", total_count)
    col_m2.metric("В процесі", sum(1 for t in st.session_state.tasks if t["status"] == "В процесі"))
    col_m3.metric("Виконано ✅", done_count)
    col_m4.metric("Борги 🚨", debts_count)

    st.markdown("---")

    # Фільтрація по предмету
    selected_subject = st.selectbox("📚 Фільтр за предметом:", SUBJECTS)

    filtered_tasks = st.session_state.tasks
    if selected_subject != "Усі предмети":
        filtered_tasks = [
            t for t in filtered_tasks if t["subject"] == selected_subject
        ]

    st.subheader("🎯 Твої завдання та квести")

    if not filtered_tasks:
        st.info("Наразі немає завдань у цій категорії. Відпочивай або перевір інші предмети!")

    for task in filtered_tasks:
        with st.container():
            col_t1, col_t2 = st.columns([4, 1])

            with col_t1:
                status_color = {
                    "Заплановано": "status-planned",
                    "В процесі": "status-process",
                    "Виконано": "status-done",
                    "Борг": "status-debt",
                }.get(task["status"], "")

                st.markdown(
                    f"### {task['subject']}: {task['title']} <span class='badge-status {status_color}'>{task['status']}</span>",
                    unsafe_allow_html=True,
                )
                st.write(task["desc"])
                if task.get("link"):
                    st.markdown(
                        f"🔗 [Перейти до матеріалів уроку]({task['link']})"
                    )

                # Інтерактивний міні-тест прямо в картці
                if task.get("quiz"):
                    with st.expander("🧩 Перевірити себе (Міні-квіз)"):
                        q = task["quiz"]
                        user_ans = st.radio(
                            q["question"], q["options"], key=f"quiz_{task['id']}"
                        )
                        if st.button("Перевірити відповідь", key=f"btn_quiz_{task['id']}"):
                            if user_ans == q["answer"]:
                                st.success("Вірно! Молодець! 🎯")
                            else:
                                st.error(
                                    f"Ні, правильна відповідь: {q['answer']}"
                                )

            with col_t2:
                # Зміна статусу учнем
                new_status = st.selectbox(
                    "Статус:",
                    ["Заплановано", "В процесі", "Виконано", "Борг"],
                    index=["Заплановано", "В процесі", "Виконано", "Борг"].index(
                        task["status"]
                    ),
                    key=f"status_select_{task['id']}",
                )
                if new_status != task["status"]:
                    task["status"] = new_status
                    save_tasks(st.session_state.tasks)
                    st.rerun()

            st.markdown("---")

# ==========================================
# 5. КАБІНЕТ МАМИ (МІСЦЕ СИЛИ RUDAFOX)
# ==========================================
else:
    st.title("👩‍🏫 Кабінет мами — Місце сили RudaFox")
    st.caption(
        "Керування навчальним планом Івана, додавання завдань та генерація звітів"
    )

    tab_add, tab_manage, tab_report = st.tabs(
        [
            "➕ Додати завдання / урок",
            "📋 Управління списком",
            "📲 Звіт у Telegram",
        ]
    )

    # Вкладка 1: Додавання нового завдання
    with tab_add:
        st.subheader("Створити новий квест / завдання")
        with st.form("new_task_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                subject = st.selectbox("Предмет:", SUBJECTS[1:])
                title = st.text_input("Назва теми / уроку:")
                date_str = st.date_input(
                    "Дата виконання:", datetime.today()
                ).strftime("%Y-%m-%d")
            with col_f2:
                link = st.text_input("Посилання на матеріали (NotebookLM / Canva / YouTube):")
                status = st.selectbox(
                    "Початковий статус:",
                    ["Заплановано", "В процесі", "Борг", "Виконано"],
                )

            desc = st.text_area("Опис завдання та інструкції для Івана:")

            st.markdown("**Додати міні-тест для самоперевірки (необов'язково):**")
            q_text = st.text_input("Запитання:")
            q_opt1 = st.text_input("Варіант 1 (Правильний):")
            q_opt2 = st.text_input("Варіант 2:")
            q_opt3 = st.text_input("Варіант 3:")

            submitted = st.form_submit_button("Зберегти завдання")

            if submitted and title:
                new_id = (
                    max([t["id"] for t in st.session_state.tasks], default=0)
                    + 1
                )
                quiz_data = None
                if q_text and q_opt1 and q_opt2:
                    options = [q_opt1, q_opt2]
                    if q_opt3:
                        options.append(q_opt3)
                    quiz_data = {
                        "question": q_text,
                        "options": sorted(options),
                        "answer": q_opt1,
                    }

                new_task = {
                    "id": new_id,
                    "subject": subject,
                    "title": title,
                    "desc": desc,
                    "status": status,
                    "link": link,
                    "date": date_str,
                    "quiz": quiz_data,
                }
                st.session_state.tasks.append(new_task)
                save_tasks(st.session_state.tasks)
                st.success(f"Завдання '{title}' успішно додано!")
                st.rerun()

    # Вкладка 2: Управління та видалення
    with tab_manage:
        st.subheader("Редагування та видалення завдань")
        for idx, t in enumerate(st.session_state.tasks):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 1])
            col_m1.write(f"**[{t['subject']}]** {t['title']}")
            col_m2.caption(f"Статус: {t['status']} | Дата: {t['date']}")
            if col_m3.button("🗑️ Видалити", key=f"del_{t['id']}"):
                st.session_state.tasks.pop(idx)
                save_tasks(st.session_state.tasks)
                st.rerun()

    # Вкладка 3: Генерація готового Telegram-повідомлення
    with tab_report:
        st.subheader("📲 Генератор щоденного звіту")
        st.write("Сформуйте гумористичний звіт для надсилання Івану або в сімейний чат:")

        debts = [t for t in st.session_state.tasks if t["status"] == "Борг"]
        dones = [
            t for t in st.session_state.tasks if t["status"] == "Виконано"
        ]
        in_progress = [
            t for t in st.session_state.tasks if t["status"] == "В процесі"
        ]

        report_msg = f"📊 **ЗВІТ НАВЧАННЯ (ІВАН, 8 КЛАС) — {datetime.now().strftime('%d.%m.%Y')}**\n\n"
        report_msg += f"✅ **Виконано ({len(dones)}):**\n"
        for d in dones:
            report_msg += f" • {d['subject']}: {d['title']}\n"

        report_msg += f"\n⏳ **В процесі ({len(in_progress)}):**\n"
        for p in in_progress:
            report_msg += f" • {p['subject']}: {p['title']}\n"

        report_msg += f"\n🚨 **Навчальні хвости ({len(debts)}):**\n"
        if debts:
            for db in debts:
                report_msg += f" • {db['subject']}: {db['title']}\n"
            report_msg += "\n*Васька чекає закритості боргів до вечора! 🐱🔥*"
        else:
            report_msg += " • Боргів немає! Абсолютний тріумф! 🎉\n"

        st.code(report_msg, language="markdown")
        st.info("Скопіюйте текст вище та надішліть в Telegram.")
