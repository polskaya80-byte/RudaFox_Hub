import json
import os
import random
from datetime import datetime
import requests
import streamlit as st

# ==========================================
# 1. ТЕМИ ОФОРМЛЕННЯ ТА CSS (З ЕДИНИМИ ШРИФТАМИ)
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
        }
        .stApp {
            background: #F5EBE0;
            background-image: radial-gradient(#E6D5C3 1.2px, transparent 0);
            background-size: 24px 24px;
        }
        [data-testid="stSidebar"] {
            background-color: #EFE3D3 !important;
            border-right: 2px dashed #B08968 !important;
        }
        [data-testid="stSidebar"] * {
            font-family: 'Comfortaa', cursive, sans-serif !important;
            color: #4A3525 !important;
        }
        h1, h2, h3, [data-testid="stSidebar"] h1 {
            font-family: 'Caveat', cursive !important;
            color: #3E2723 !important;
            font-weight: 700 !important;
        }
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
            padding: 18px;
            color: #5C3D2E;
            margin-bottom: 22px;
        }
        .stButton>button {
            border-radius: 12px !important;
            border: 2px solid #4A3525 !important;
            background-color: #81B29A !important;
            color: #FFFFFF !important;
            font-family: 'Comfortaa', sans-serif !important;
            font-weight: 700 !important;
            box-shadow: 3px 3px 0px #4A3525 !important;
        }
    """,
    "🎮 Cyberpunk / Gaming": """
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif !important;
            background-color: #0F172A !important;
            color: #F8FAFC !important;
        }
        .stApp { background: #0F172A; }
        [data-testid="stSidebar"] { background-color: #1E293B !important; }
        [data-testid="stSidebar"] * { color: #F8FAFC !important; }
        h1, h2, h3 { color: #38BDF8 !important; }
        .craft-card { background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 18px; }
        .quote-craft { background-color: #1E1B4B; border-left: 4px solid #818CF8; padding: 16px; color: #E0E7FF; margin-bottom: 20px; }
        .stButton>button { background-color: #0284C7 !important; color: #FFFFFF !important; border: none !important; }
    """,
}

# ==========================================
# 2. ФАЙЛИ ТА ЗБЕРЕЖЕННЯ
# ==========================================
DATA_FILE = "tasks_db.json"
CONFIG_FILE = "config.json"

DEFAULT_TASKS = [
    {
        "id": 1,
        "subject": "Географія",
        "title": "Чинники розміщення виробництв",
        "desc": "Складові економічної географії: чому заводи будують біля сировини або біля споживачів.",
        "content_body": "### 📖 Теоретичний конспект\nПри розміщенні підприємств враховують **сировинний, паливний, трудовий та споживчий чинники**. Для важкої металургії головним є орієнтація на руду та вугілля, а для пекарень — на споживача.",
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
                "hint": "Потребує металу та ринок збуту.",
                "explanation": "Важке машинобудування орієнтується на бази металургії та споживача.",
            }
        ],
    }
]

TEEN_FOCUS_TIPS = [
    "🧠 **Лайфхак фокусу:** 25 хвилин інтенсивної роботи + 5 хвилин відпочинку (техніка Pomodoro) залишають максимум дофаміну на вечір.",
    "🎯 **Автономія:** Ти сам керуєш своїм розкладом. Закрий складні квести першими — і решта дня повністю твоя.",
    "💡 **Нейрофізіологія:** Складні завдання краще розбивати на 2-3 мікро-кроки. Мозок не любить невизначеності.",
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
            "gemini_api_key": "",
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
# 3. TELEGRAM ТА GEMINI ШІ-ГЕНЕРАЦІЯ
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


def generate_lesson_with_gemini(
    subject, title, teacher_prompt, raw_sources, aspects, num_q, mode
):
    """Генерує конспект уроку та тестові питання через Gemini API або резервну логіку"""
    api_key = st.session_state.config.get("gemini_api_key", "").strip()

    system_prompt = f"""
    Ти — досвідчений педагог для 9 класу. Твій стиль викладання: {teacher_prompt}.
    Створи навчальний комплект для уроку '{title}' з предмета '{subject}'.
    Згенеруй JSON об'єкт з ключами:
    1. "desc": короткий мотивуючий опис завдання для учня (1-2 речення).
    2. "content_body": цікавий, глибокий та структурований конспект уроку (Markdown).
    3. "quiz": масив з {num_q} реальних запитань за аспекти ({', '.join(aspects)}).
    Кожне питання має бути у форматі об'єкта з ключами: "question", "options" (масив з 3 варіантів), "answer" (строго точний варіант з варіантів), "hint" (корисна підказка), "explanation" (педагогічне пояснення).
    Джерела та матеріали теми: {raw_sources}
    """

    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": system_prompt}]}]}
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                text_res = res.json()["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                start = text_res.find("{")
                end = text_res.rfind("}") + 1
                parsed = json.loads(text_res[start:end])
                return (
                    parsed.get("desc", ""),
                    parsed.get("content_body", ""),
                    parsed.get("quiz", []),
                )
        except Exception:
            pass

    # Локальний резервний формат
    quiz_list = []
    for i in range(1, num_q + 1):
        asp = aspects[(i - 1) % len(aspects)]
        quiz_list.append(
            {
                "question": f"Тестове запитання №{i} за темою '{title}' ({asp})",
                "options": [
                    f"Правильна відповідь {i}",
                    f"Варіант B{i}",
                    f"Варіант C{i}",
                ],
                "answer": f"Правильна відповідь {i}",
                "hint": f"Підказка щодо {asp}.",
                "explanation": f"Обґрунтування правильної відповіді №{i}.",
            }
        )

    content_body = f"### 📖 Конспект уроку: {title}\n\nОпрацюйте надані джерела. {teacher_prompt}\n\n**Матеріали:**\n{raw_sources}"
    desc = f"Вивчити тему '{title}' та пройти підсумковий тест."
    return desc, content_body, quiz_list


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
# 4. БІЧНА ПАНЕЛЬ
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
            st.write(f"📌 **Завдання:** {task['desc']}")

            if task.get("content_body"):
                with st.expander("📖 Читати теоретичний конспект уроку"):
                    st.markdown(task["content_body"])

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
                    f"🧩 Інтерактивний тест ({task.get('mode', 'Контрольний')}) — {len(quiz_list)} питань"
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
            "⚙️ Налаштування ШІ & Telegram",
        ]
    )

    with tab_create:
        st.subheader("➕ Створити / Згенерувати урок")

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

            st.markdown("---")
            st.markdown("### 📚 Джерела та Матеріали")
            t_file = st.file_uploader(
                "Завантажити файл джерела (PDF / TXT / DOCX):",
                type=["pdf", "txt", "docx"],
            )
            raw_text = st.text_area("Скопійований конспект / текст теми:")
            t_links = st.text_input("Основне посилання (NotebookLM, сайт):")
            t_pres = st.text_input("Посилання на Презентацію NotebookLM:")
            t_video = st.text_input("Посилання на відео:")

            st.markdown("---")
            st.markdown("### 🤖 Бачення вчителя та Налаштування Тесту")
            teacher_prompt = st.text_area(
                "Бачення вчителя (стиль, тон, ключові акценти):"
            )

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                num_q = st.slider(
                    "Кількість запитань у тесті (від 1 до 24):", 1, 24, 5
                )
            with col_q2:
                aspects = st.multiselect(
                    "🎯 Аспекти перевірки знань:",
                    [
                        "Дати та Події",
                        "Концепції та Теореми",
                        "Критичне мислення",
                        "Логіка та Формули",
                        "Термінологія",
                        "Практичні задачі",
                    ],
                    default=["Концепції та Теореми", "Термінологія"],
                )

            btn_save = st.form_submit_button("✨ Згенерувати комплект уроку")

            if btn_save and t_title:
                mode_clean = (
                    "Тренувальний" if "Тренувальний" in t_mode else "Контрольний"
                )

                file_str = ""
                if t_file:
                    try:
                        file_str = t_file.read().decode("utf-8", errors="ignore")
                    except Exception:
                        file_str = "Зміст файлу"

                full_sources = f"{raw_text}\n{file_str}"

                gen_desc, gen_body, gen_quiz = generate_lesson_with_gemini(
                    subj,
                    t_title,
                    teacher_prompt,
                    full_sources,
                    aspects,
                    num_q,
                    mode_clean,
                )

                new_id = (
                    max([t["id"] for t in st.session_state.tasks], default=0)
                    + 1
                )
                new_task = {
                    "id": new_id,
                    "subject": subj,
                    "title": t_title,
                    "desc": gen_desc,
                    "content_body": gen_body,
                    "status": t_status,
                    "link": t_links,
                    "presentation_link": t_pres,
                    "video_url": t_video,
                    "mode": mode_clean,
                    "date": t_date,
                    "aspects": aspects,
                    "quiz": gen_quiz,
                }
                st.session_state.tasks.append(new_task)
                save_data(DATA_FILE, st.session_state.tasks)
                st.success(f"✨ Комплект уроку '{t_title}' успішно додано!")
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
        st.subheader("⚙️ Налаштування ШІ & Telegram")
        with st.form("settings_form"):
            st.markdown("### 🔑 1. Ключ ШІ (Google Gemini API)")
            g_key = st.text_input(
                "Вставте сюди свій Gemini API Key (починається з AIzaSy...):",
                value=st.session_state.config.get("gemini_api_key", ""),
                type="password",
            )
            st.markdown("---")
            st.markdown("### 📲 2. Сповіщення в Telegram")
            t_token = st.text_input(
                "Telegram Bot Token:",
                value=st.session_state.config.get("bot_token", ""),
                type="password",
            )
            t_chat = st.text_input(
                "Telegram Chat ID:",
                value=st.session_state.config.get("chat_id", ""),
            )
            if st.form_submit_button("💾 Зберегти всі налаштування"):
                st.session_state.config["gemini_api_key"] = g_key
                st.session_state.config["bot_token"] = t_token
                st.session_state.config["chat_id"] = t_chat
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Налаштування збережено! ШІ повністю активовано.")
                st.rerun()
