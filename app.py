import json
import os
import random
from datetime import datetime
import requests
import streamlit as st

# ==========================================
# 1. ТЕМИ ОФОРМЛЕННЯ ТА НАВЕДЕННЯ ЛАДУ В ШРИФТАХ
# ==========================================
st.set_page_config(
    page_title="RudaFox - Навчальний Хаб 9 Клас",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEMES = {
    "📜 Крафт & Скетч": """
        @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Comfortaa:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Comfortaa', cursive, sans-serif !important;
            background-color: #F5EBE0 !important;
            color: #4A3525 !important;
            line-height: 1.6;
        }
        .stApp {
            background: #F5EBE0;
            background-image: radial-gradient(#E6D5C3 1.2px, transparent 0);
            background-size: 24px 24px;
        }
        h1, h2, h3 {
            font-family: 'Caveat', cursive !important;
            color: #3E2723 !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px;
        }
        h1 { font-size: 2.6rem !important; margin-bottom: 0.5rem !important; }
        h2 { font-size: 2.0rem !important; }
        h3 { font-size: 1.6rem !important; }
        
        .craft-card {
            background-color: #FFFDF9;
            border: 2px dashed #B08968;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 4px 4px 0px #DDB892;
        }
        .quote-craft {
            background-color: #FFF8E1;
            border: 2px solid #E07A5F;
            border-radius: 14px;
            padding: 18px 22px;
            color: #5C3D2E;
            font-size: 0.95rem;
            margin-bottom: 22px;
            box-shadow: 2px 2px 0px #E07A5F;
        }
        .stButton>button {
            border-radius: 12px !important;
            border: 2px solid #4A3525 !important;
            background-color: #81B29A !important;
            color: #FFFFFF !important;
            font-family: 'Comfortaa', sans-serif !important;
            font-weight: 700 !important;
            padding: 8px 18px !important;
            box-shadow: 3px 3px 0px #4A3525 !important;
        }
        .stButton>button:hover {
            transform: translate(-1px, -1px);
            box-shadow: 4px 4px 0px #4A3525 !important;
            background-color: #6B8E23 !important;
        }
    """,
    "🎮 Cyberpunk / Gaming": """
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif !important;
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            line-height: 1.5;
        }
        .stApp { background: #0F172A; }
        h1, h2, h3 { color: #38BDF8 !important; font-weight: 700 !important; }
        .craft-card {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .quote-craft {
            background-color: #1E1B4B;
            border-left: 4px solid #818CF8;
            border-radius: 8px;
            padding: 16px;
            color: #E0E7FF;
            margin-bottom: 20px;
        }
        .stButton>button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
    """,
    "☕ Lo-Fi Study Space": """
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Quicksand', sans-serif !important;
            background-color: #EAE7DC !important;
            color: #474747 !important;
            line-height: 1.6;
        }
        .stApp { background: #EAE7DC; }
        h1, h2, h3 { color: #E85A4F !important; font-weight: 700 !important; }
        .craft-card {
            background-color: #F8F5F0;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 18px;
            border: 1px solid #D8D3CD;
        }
        .quote-craft {
            background-color: #D8C3A5;
            border-radius: 10px;
            padding: 16px;
            color: #333333;
            margin-bottom: 20px;
        }
        .stButton>button {
            border-radius: 10px !important;
            border: none !important;
            background-color: #E85A4F !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
    """,
    "⚡ Minimal Tech": """
        html, body, [class*="css"] {
            background-color: #FAFAFA !important;
            color: #171717 !important;
            line-height: 1.5;
        }
        .stApp { background: #FAFAFA; }
        h1, h2, h3 { color: #0A0A0A !important; font-weight: 700 !important; }
        .craft-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 18px;
        }
        .quote-craft {
            background-color: #F5F5F5;
            border-left: 3px solid #171717;
            padding: 16px;
            margin-bottom: 20px;
        }
        .stButton>button {
            border-radius: 6px !important;
            background-color: #171717 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
    """,
}

# ==========================================
# 2. ФАЙЛИ ТА НАЛАШТУВАННЯ
# ==========================================
DATA_FILE = "tasks_db.json"
CONFIG_FILE = "config.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "subject": "Географія",
        "title": "Чинники розміщення виробництв",
        "desc": "Опрацювати матеріали уроку, переглянути презентацію в NotebookLM та пройти тест.",
        "status": "В процесі",
        "link": "https://notebooklm.google.com/notebook/3eb94634-62b1-4c57-8d6b-fe3bb2343692",
        "presentation_link": "https://notebooklm.google.com/notebook/3eb94634-62b1-4c57-8d6b-fe3bb2343692",
        "video_url": "",
        "date": "2026-10-19",
        "aspects": ["Концепції", "Термінологія"],
        "mode": "Контрольний",
        "quiz": [
            {
                "question": "Який чинник є вирішальним для розміщення підприємств важкого машинобудування?",
                "options": [
                    "Сировинний та споживчий",
                    "Трудовий чинник",
                    "Водний чинник",
                ],
                "answer": "Сировинний та споживчий",
                "hint": "Потребує багато металу та ринок збуту.",
                "explanation": "Важке машинобудування орієнтується на бази металургії та споживача.",
            }
        ],
    }
]

TEEN_FOCUS_TIPS = [
    "🧠 **Лайфхак фокусу:** 25 хвилин інтенсивної роботи + 5 хвилин відпочинку (техніка Pomodoro) залишають максимум дофаміну на вечір.",
    "🎯 **Автономія:** Ти сам керуєш своїм розкладом. Закрий складні квести першими — і решта дня повністю твоя.",
    "💡 **Нейрофізіологія:** Складні завдання краще розбивати на 2-3 мікро-кроки. Мозок не любить невизначеності.",
    "⚡ **Ефективність:** Якісна концентрація протягом 30 хвилин дає кращий результат, ніж 2 години відволікань.",
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
        CONFIG_FILE,
        {
            "bot_token": "",
            "chat_id": "",
            "theme": "📜 Крафт & Скетч",
            "custom_css": "",
        },
    )

selected_theme = st.session_state.config.get("theme", "📜 Крафт & Скетч")
custom_css = st.session_state.config.get("custom_css", "")

st.markdown(
    f"<style>{THEMES.get(selected_theme, THEMES['📜 Крафт & Скетч'])}\n{custom_css}</style>",
    unsafe_allow_html=True,
)


# ==========================================
# 3. TELEGRAM АВТО-ЗВІТНІСТЬ
# ==========================================
def send_telegram_msg(text):
    token = st.session_state.config.get("bot_token")
    chat_id = st.session_state.config.get("chat_id")
    if not token or not chat_id:
        return False, "⚠️ Вкажіть Bot Token та Chat ID у Налаштуваннях!"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(
            url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )
        if res.status_code == 200:
            return True, "🚀 Звіт надіслано в Телеграм!"
        else:
            return False, f"Помилка Телеграм API: {res.text}"
    except Exception as e:
        return False, f"Помилка з'єднання: {e}"


def build_interactive_html_test(quiz_list, mode, subject, title):
    quiz_json = json.dumps(quiz_list, ensure_ascii=False)
    html_code = (
        '<!DOCTYPE html>\n'
        '<html>\n'
        '<head>\n'
        '    <meta charset="utf-8">\n'
        '    <style>\n'
        '        body { font-family: sans-serif; background: #0F172A; color: #F8FAFC; padding: 20px; }\n'
        '        .card { background: #1E293B; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #334155; }\n'
        '        .btn { background: #0284C7; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 10px; }\n'
        '        .hint { background: #312E81; padding: 8px; border-radius: 4px; margin-top: 8px; display: none; }\n'
        '        .exp { padding: 8px; border-radius: 4px; margin-top: 8px; display: none; }\n'
        '    </style>\n'
        '</head>\n'
        '<body>\n'
        f'    <h2>🧩 Тест ({mode}): {subject} - {title}</h2>\n'
        '    <div id="quiz-root"></div>\n'
        '    <script>\n'
        f'        const data = {quiz_json};\n'
        '        const root = document.getElementById("quiz-root");\n'
        '        data.forEach((q, i) => {\n'
        '            let div = document.createElement("div");\n'
        '            div.className = "card";\n'
        '            let html = "<b>Q" + (i+1) + ": " + q.question + "</b><br><br>";\n'
        '            q.options.forEach(opt => {\n'
        '                html += \'<label style="display:block;margin:4px 0;"><input type="radio" name="q_\'+i+\'" value="\'+opt+\'"> \'+opt+\'</label>\';\n'
        '            });\n'
        '            html += \'<button class="btn" style="background:#4338CA;margin-right:8px;" onclick="document.getElementById(\\\\\'h_\'+i+\'\\\\\').style.display=\\\\\'block\\\\\'">💡 Підказка</button>\';\n'
        '            html += \'<button class="btn" onclick="check(\'+i+\')">Перевірити</button>\';\n'
        '            html += \'<div id="h_\'+i+\'" class="hint">🔑 \' + (q.hint || \'\') + \'</div>\';\n'
        '            html += \'<div id="e_\'+i+\'" class="exp"></div>\';\n'
        '            div.innerHTML = html;\n'
        '            root.appendChild(div);\n'
        '        });\n'
        '        function check(i) {\n'
        '            let sel = document.querySelector(\'input[name="q_\'+i+\'"]:checked\');\n'
        '            let exp = document.getElementById(\'e_\'+i);\n'
        '            if (!sel) return alert(\'Оберіть відповідь!\');\n'
        '            if (sel.value === data[i].answer) {\n'
        '                exp.innerHTML = \'✨ Правильно! \' + (data[i].explanation || \'\');\n'
        '                exp.style.background = \'#065F46\';\n'
        '            } else {\n'
        '                exp.innerHTML = \'❌ Невірно. Правильна відповідь: \' + data[i].answer + \'. \' + (data[i].explanation || \'\');\n'
        '                exp.style.background = \'#991B1B\';\n'
        '            }\n'
        '            exp.style.display = \'block\';\n'
        '        }\n'
        '    </script>\n'
        '</body>\n'
        '</html>\n'
    )
    return html_code


# ==========================================
# 4. БІЧНА ПАНЕЛЬ (ОНОВЛЕНІ НАЗВИ ПРОСТОРІВ)
# ==========================================
st.sidebar.markdown("# 🦊 RudaFox Hub")
st.sidebar.caption("🎓 Навчальний простір 9 класу")

role = st.sidebar.radio(
    "📍 Оберіть простір:",
    [
        "👦 Місце страждань та досягнень Іванка Миколайовича",
        "👩‍🏫 Місце сили RudaFox",
    ],
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
# 5. МІСЦЕ СТРАЖДАНЬ ТА ДОСЯГНЕНЬ ІВАНКА МИКОЛАЙОВИЧА
# ==========================================
if role == "👦 Місце страждань та досягнень Іванка Миколайовича":
    st.title("📜 Місце страждань та досягнень Іванка Миколайовича")

    st.markdown(
        f'<div class="quote-craft">{random.choice(TEEN_FOCUS_TIPS)}</div>',
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
    col1.metric("Заплановано уроків", total_count)
    col2.metric("Виконано ✅", done_count)
    col3.metric("Хвости 🚨", debts_count)

    st.markdown("---")
    selected_subject = st.selectbox("🔍 Предмет:", SUBJECTS)

    filtered = st.session_state.tasks
    if selected_subject != "Усі предмети":
        filtered = [t for t in filtered if t["subject"] == selected_subject]

    st.subheader("📚 Твої квести та завдання")

    if not filtered:
        st.info("Немає завдань у цій категорії.")

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
                st.markdown(f"🔗 [Основні матеріали уроку]({task['link']})")

            if task.get("presentation_link"):
                st.markdown(
                    f"📊 [Презентація / Флеш-картки NotebookLM]({task['presentation_link']})"
                )

            if task.get("video_url"):
                st.markdown(
                    f"🎬 [Дивитися відеопояснення]({task['video_url']})"
                )

            quiz_list = task.get("quiz", [])
            user_score = 0
            max_score = max(len(quiz_list), 1)

            if quiz_list:
                with st.expander(
                    f"🧩 Інтерактивний тест ({task.get('mode', 'Контрольний')})"
                ):
                    for q_idx, q in enumerate(quiz_list):
                        st.markdown(
                            f"**Питання {q_idx + 1}:** {q['question']}"
                        )
                        u_choice = st.radio(
                            "Відповідь:",
                            q["options"],
                            key=f"task_{task['id']}_q_{q_idx}",
                        )

                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(
                                f"💡 Підказка Q{q_idx+1}",
                                key=f"h_btn_{task['id']}_{q_idx}",
                            ):
                                st.info(f"🔑 {q.get('hint', '')}")
                        with col_btn2:
                            if st.button(
                                f"Перевірити Q{q_idx+1}",
                                key=f"c_btn_{task['id']}_{q_idx}",
                            ):
                                if u_choice == q["answer"]:
                                    st.success("✨ Вірно!")
                                    user_score += 1
                                else:
                                    st.error("❌ Невірно.")
                                    st.warning(f"💡 {q.get('explanation', '')}")
                        st.markdown("---")

            html_content = build_interactive_html_test(
                quiz_list,
                task.get("mode", "Контрольний"),
                task["subject"],
                task["title"],
            )
            st.download_button(
                label="📥 Скачати HTML-тест",
                data=html_content,
                file_name=f"test_{task['subject']}_{task['id']}.html",
                mime="text/html",
                key=f"dl_html_{task['id']}",
            )

        with col_b:
            st.write("**Статус:**")
            mode_str = task.get("mode", "Контрольний")
            st.caption(f"⚙️ Режим: **{mode_str}**")

            if task["status"] != "Виконано":
                if st.button(
                    "✅ Завершити урок", key=f"finish_btn_{task['id']}"
                ):
                    task["status"] = "Виконано"
                    save_data(DATA_FILE, st.session_state.tasks)

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
                    score_pct = int((user_score / max_score) * 100)
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # ТОЧНИЙ КАСКАДНИЙ ЗВІТ
                    tg_report = (
                        f"🦊 **ЗВІТ З МІСЦЯ СТРАЖДАНЬ ТА ДОСЯГНЕНЬ**\n\n"
                        f"📚 **Предмет:** {task['subject']}\n"
                        f"📖 **Тема:** {task['title']}\n"
                        f"🏋️‍♂️ **Режим:** {mode_str}\n"
                        f"📊 **Результат тесту:** {score_pct}% ({user_score}/{max_score})\n"
                        f"📈 **Прогрес за день:** {new_done_count} з {len(st.session_state.tasks)} уроків закрито ({daily_pct}%)\n"
                        f"⏰ **Час здачі:** {now_str}"
                    )

                    st.balloons()
                    send_telegram_msg(tg_report)
                    st.success("🎉 Звіт відправлено в Телеграм!")
                    st.rerun()
            else:
                st.success("Завершено ✅")

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. МІСЦЕ СИЛИ RUDAFOX
# ==========================================
else:
    st.title("👩‍🏫 Місце сили RudaFox")

    tab_create, tab_manage, tab_style, tab_settings = st.tabs(
        [
            "🛠️ Конструктор Уроку",
            "📋 Управління уроками",
            "🎨 Кастомізація дизайну",
            "⚙️ Налаштування Telegram",
        ]
    )

    with tab_create:
        st.subheader("➕ Створити новий урок")

        with st.form("teacher_lesson_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                subj = st.selectbox("Предмет:", SUBJECTS[1:])
                t_title = st.text_input("Назва теми:")
                t_date = st.date_input(
                    "Дата виконання:", datetime.today()
                ).strftime("%Y-%m-%d")
            with col_f2:
                t_mode = st.selectbox(
                    "Режим тестування:",
                    [
                        "🏋️‍♂️ Тренувальний (з підказками)",
                        "⏱️ Контрольний",
                    ],
                )
                t_status = st.selectbox(
                    "Початковий статус:",
                    ["Заплановано", "В процесі", "Борг", "Виконано"],
                )

            t_desc = st.text_area("Опис завдання для Івана:")

            st.markdown("---")
            st.markdown("### 📚 Джерела та Презентації")
            t_links = st.text_input("Основне посилання (NotebookLM, сайт):")
            t_pres = st.text_input("Посилання на Презентацію NotebookLM:")
            t_video = st.text_input("Посилання на відео:")

            st.markdown("---")
            st.markdown("### 🧩 Налаштування Тестування")
            q_text = st.text_input("Запитання:")
            q_opt1 = st.text_input("Варіант 1 (Правильний):")
            q_opt2 = st.text_input("Варіант 2:")
            q_opt3 = st.text_input("Варіант 3:")
            q_hint = st.text_input("💡 Підказка:")
            q_exp = st.text_area("💡 Пояснення відповіді:")

            btn_save = st.form_submit_button("💾 Зберегти урок в хаб")

            if btn_save and t_title:
                mode_clean = (
                    "Тренувальний" if "Тренувальний" in t_mode else "Контрольний"
                )
                quiz_obj = []
                if q_text and q_opt1 and q_opt2:
                    opts = [q_opt1, q_opt2]
                    if q_opt3:
                        opts.append(q_opt3)
                    quiz_obj = [
                        {
                            "question": q_text,
                            "options": sorted(opts),
                            "answer": q_opt1,
                            "hint": q_hint,
                            "explanation": q_exp,
                        }
                    ]

                new_id = (
                    max([t["id"] for t in st.session_state.tasks], default=0)
                    + 1
                )
                new_task = {
                    "id": new_id,
                    "subject": subj,
                    "title": t_title,
                    "desc": t_desc,
                    "status": t_status,
                    "link": t_links,
                    "presentation_link": t_pres,
                    "video_url": t_video,
                    "mode": mode_clean,
                    "date": t_date,
                    "quiz": quiz_obj,
                }
                st.session_state.tasks.append(new_task)
                save_data(DATA_FILE, st.session_state.tasks)
                st.success(f"✨ Урок '{t_title}' успішно додано!")
                st.rerun()

    with tab_manage:
        st.subheader("📋 Список усіх уроків")
        for idx, task in enumerate(st.session_state.tasks):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 1])
            col_m1.write(f"**[{task['subject']}]** {task['title']}")
            col_m2.caption(f"Питань у тесті: {len(task.get('quiz', []))}")
            if col_m3.button("🗑️ Видалити", key=f"del_task_{task['id']}"):
                st.session_state.tasks.pop(idx)
                save_data(DATA_FILE, st.session_state.tasks)
                st.rerun()

    with tab_style:
        st.subheader("🎨 Кастомізація дизайну")
        with st.form("style_form"):
            theme_choice = st.selectbox(
                "Шаблон оформлення:",
                list(THEMES.keys()),
                index=list(THEMES.keys()).index(
                    st.session_state.config.get("theme", "📜 Крафт & Скетч")
                ),
            )
            custom_css_input = st.text_area(
                "Власний CSS / Стильовий промпт:",
                value=st.session_state.config.get("custom_css", ""),
            )

            if st.form_submit_button("💾 Зберегти новий дизайн"):
                st.session_state.config["theme"] = theme_choice
                st.session_state.config["custom_css"] = custom_css_input
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Новий дизайн застосовано!")
                st.rerun()

    with tab_settings:
        st.subheader("⚙️ Telegram Налаштування")
        with st.form("settings_form"):
            t_token = st.text_input(
                "Telegram Bot Token:",
                value=st.session_state.config.get("bot_token", ""),
                type="password",
            )
            t_chat = st.text_input(
                "Telegram Chat ID:",
                value=st.session_state.config.get("chat_id", ""),
            )
            if st.form_submit_button("💾 Зберегти налаштування"):
                st.session_state.config["bot_token"] = t_token
                st.session_state.config["chat_id"] = t_chat
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Налаштування збережено!")
