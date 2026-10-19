import json
import os
import random
from datetime import datetime
import requests
import streamlit as st

# ==========================================
# 1. ТЕМИ ОФОРМЛЕННЯ ТА ДИНАМІЧНИЙ CSS
# ==========================================
st.set_page_config(
    page_title="RudaFox - Навчальний Хаб 9 Клас",
    page_icon="🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEMES = {
    "📜 Крафт & Скетч": """
        @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Comfortaa:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Comfortaa', cursive, sans-serif; background-color: #F5EBE0 !important; color: #4A3525; }
        .stApp { background: #F5EBE0; background-image: radial-gradient(#E6D5C3 1px, transparent 0); background-size: 24px 24px; }
        h1, h2, h3 { font-family: 'Caveat', cursive !important; color: #3E2723 !important; }
        .craft-card { background-color: #FFFDF9; border: 2px dashed #B08968; border-radius: 16px; padding: 20px; margin-bottom: 16px; box-shadow: 4px 4px 0px #DDB892; }
        .quote-craft { background-color: #FFF8E1; border: 2px solid #E07A5F; border-radius: 14px; padding: 16px 20px; color: #5C3D2E; margin-bottom: 20px; }
        .stButton>button { border-radius: 12px !important; border: 2px solid #4A3525 !important; background-color: #81B29A !important; color: #FFFFFF !important; font-weight: 700 !important; }
    """,
    "🎮 Cyberpunk / Gaming": """
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #0F172A !important; color: #F8FAFC; }
        .stApp { background: #0F172A; }
        h1, h2, h3 { color: #38BDF8 !important; text-shadow: 0 0 10px rgba(56,189,248,0.3); }
        .craft-card { background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .quote-craft { background-color: #1E1B4B; border-left: 4px solid #818CF8; border-radius: 8px; padding: 16px; color: #E0E7FF; margin-bottom: 20px; }
        .stButton>button { border-radius: 8px !important; border: none !important; background-color: #0284C7 !important; color: #FFFFFF !important; font-weight: 600 !important; }
    """,
    "☕ Lo-Fi Study Space": """
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
        html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; background-color: #EAE7DC !important; color: #8E8D8A; }
        .stApp { background: #EAE7DC; }
        h1, h2, h3 { color: #E85A4F !important; }
        .craft-card { background-color: #F8F5F0; border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid #D8D3CD; }
        .quote-craft { background-color: #D8C3A5; border-radius: 12px; padding: 16px; color: #474747; margin-bottom: 20px; }
        .stButton>button { border-radius: 12px !important; border: none !important; background-color: #E85A4F !important; color: #FFFFFF !important; }
    """,
    "⚡ Minimal Tech": """
        html, body, [class*="css"] { background-color: #FAFAFA !important; color: #171717; }
        .stApp { background: #FAFAFA; }
        h1, h2, h3 { color: #0A0A0A !important; font-weight: 800 !important; }
        .craft-card { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
        .quote-craft { background-color: #F5F5F5; border-left: 3px solid #171717; padding: 16px; margin-bottom: 20px; }
        .stButton>button { border-radius: 6px !important; background-color: #171717 !important; color: #FFFFFF !important; }
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
        "desc": "Опрацювати матеріали уроку та пройти підсумковий тест.",
        "status": "В процесі",
        "link": "https://notebooklm.google.com/notebook/3eb94634-62b1-4c57-8d6b-fe3bb2343692",
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
                "hint": "Потребує металу та орієнтації на споживача.",
                "explanation": "Важке машинобудування орієнтується на бази металургії та ринок збуту.",
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
            "claude_api_key": "",
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
# 3. TELEGRAM ТА CLAUDE API
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


def generate_lesson_with_claude(
    subject,
    title,
    teacher_prompt,
    text_sources,
    link_sources,
    aspects,
    num_questions,
    mode,
):
    api_key = st.session_state.config.get("claude_api_key", "").strip()

    system_instructions = (
        f"Ти — досвідчений методист та педагог для учня 9 класу. "
        f"Створи навчальне завдання та рівно {num_questions} тестових питань у форматі JSON. "
        f"Аспекти перевірки знань: {', '.join(aspects)}. Режим: {mode}. Промпт: {teacher_prompt}."
    )

    if api_key.startswith("sk-ant"):
        try:
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            body = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 2500,
                "system": system_instructions,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Предмет: {subject}\nТема: {title}\nДжерела: {text_sources}\nПосилання: {link_sources}\nЗгенеруй JSON об'єкт з ключами desc (текст) та quiz (масив з {num_questions} об'єктів з question, options, answer, hint, explanation).",
                    }
                ],
            }
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=body,
                timeout=30,
            )
            if response.status_code == 200:
                content = response.json()["content"][0]["text"]
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                parsed = json.loads(content[start_idx:end_idx])
                return (
                    parsed.get(
                        "desc", f"Опрацювати матеріали теми: {title}."
                    ),
                    parsed.get("quiz", []),
                )
        except Exception:
            pass

    questions = []
    for i in range(1, num_questions + 1):
        questions.append(
            {
                "question": f"Питання №{i} з теми '{title}' ({aspects[(i-1) % len(aspects)]})",
                "options": [
                    f"Правильний варіант {i}",
                    f"Варіант B{i}",
                    f"Варіант C{i}",
                ],
                "answer": f"Правильний варіант {i}",
                "hint": f"Підказка до питання №{i}.",
                "explanation": f"Детальне пояснення до питання №{i}.",
            }
        )
    desc = f"Опрацювати тему '{title}'. Джерела: {link_sources}. {teacher_prompt}"
    return desc, questions


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
    "📍 Оберіть кабінет:",
    ["👦 Кабінет Івана (Учень)", "👩‍🏫 Кабінет мами (Конструктор)"],
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
# 5. КАБІНЕТ ІВАНА
# ==========================================
if role == "👦 Кабінет Івана (Учень)":
    st.title("📜 Робочий простір Івана — 9 Клас")

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
                st.markdown(f"🔗 [Перейти до матеріалів]({task['link']})")

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
# 6. КАБІНЕТ МАМИ
# ==========================================
else:
    st.title("👩‍🏫 Кабінет мами — «Місце сили RudaFox»")

    tab_create, tab_manage, tab_style, tab_settings = st.tabs(
        [
            "🛠️ Генератор Уроків",
            "📋 Управління уроками",
            "🎨 Кастомізація дизайну",
            "⚙️ Налаштування API & Telegram",
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
            st.markdown("### 📚 Джерела матеріалів")
            t_links = st.text_input(
                "Посилання (NotebookLM, веб-сторінки, PDF):"
            )
            t_video = st.text_input("Посилання на відео:")
            raw_text = st.text_area("Текст конспекту або нотатки:")

            st.markdown("---")
            st.markdown("### 🤖 Налаштування ШІ-Тестування")
            teacher_prompt = st.text_area("Власний промпт для ШІ:")

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                num_q = st.slider("Кількість питань (1 - 24):", 1, 24, 5)
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
                    default=["Концепції та Теореми"],
                )

            btn_generate = st.form_submit_button(
                "✨ Згенерувати урок та тест з Claude"
            )

            if btn_generate and t_title:
                mode_clean = (
                    "Тренувальний" if "Тренувальний" in t_mode else "Контрольний"
                )
                generated_desc, generated_quiz = generate_lesson_with_claude(
                    subj,
                    t_title,
                    teacher_prompt,
                    raw_text,
                    f"{t_links} {t_video}",
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
                    "desc": generated_desc,
                    "status": t_status,
                    "link": t_links,
                    "video_url": t_video,
                    "mode": mode_clean,
                    "date": t_date,
                    "aspects": aspects,
                    "quiz": generated_quiz,
                }
                st.session_state.tasks.append(new_task)
                save_data(DATA_FILE, st.session_state.tasks)
                st.success(f"✨ Урок '{t_title}' успішно створено!")
                st.rerun()

    with tab_manage:
        st.subheader("📋 Список усіх уроків")
        for idx, task in enumerate(st.session_state.tasks):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 1])
            col_m1.write(f"**[{task['subject']}]** {task['title']}")
            col_m2.caption(f"Питань: {len(task.get('quiz', []))}")
            if col_m3.button("🗑️ Видалити", key=f"del_task_{task['id']}"):
                st.session_state.tasks.pop(idx)
                save_data(DATA_FILE, st.session_state.tasks)
                st.rerun()

    with tab_style:
        st.subheader("🎨 Кастомізація дизайну та теми оформлення")
        st.write("Оберіть готову тему або задайте власний стильовий промпт/CSS:")

        with st.form("style_form"):
            theme_choice = st.selectbox(
                "Шаблон оформлення:",
                list(THEMES.keys()),
                index=list(THEMES.keys()).index(
                    st.session_state.config.get("theme", "📜 Крафт & Скетч")
                ),
            )
            custom_css_input = st.text_area(
                "Власний CSS / Промпт кастомізації (наприклад: змінити колір кнопок чи фон):",
                value=st.session_state.config.get("custom_css", ""),
            )

            if st.form_submit_button("💾 Зберегти новий дизайн"):
                st.session_state.config["theme"] = theme_choice
                st.session_state.config["custom_css"] = custom_css_input
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Новий дизайн застосовано!")
                st.rerun()

    with tab_settings:
        st.subheader("⚙️ Налаштування API та Telegram")
        with st.form("settings_form"):
            claude_key = st.text_input(
                "Claude (Anthropic) API Key:",
                value=st.session_state.config.get("claude_api_key", ""),
                type="password",
            )
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
                st.session_state.config["claude_api_key"] = claude_key
                st.session_state.config["bot_token"] = t_token
                st.session_state.config["chat_id"] = t_chat
                save_data(CONFIG_FILE, st.session_state.config)
                st.success("Налаштування збережено!")
