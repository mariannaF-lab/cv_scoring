import os
import streamlit as st
from openai import OpenAI
from parse_hh import get_html, extract_vacancy_data, extract_resume_data

def get_api_key() -> str | None:
    # 1) пробуем переменную окружения — не трогает парсер secrets
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    # 2) пробуем st.secrets, если .streamlit/secrets.toml на месте
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None

API_KEY = get_api_key()
if not API_KEY:
    st.error(
        "Не найден OPENAI_API_KEY. "
        "Добавьте его в .streamlit/secrets.toml или задайте переменную окружения."
    )
    st.stop()

client = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.
Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). 
Эта оценка должна учитываться при выставлении финальной оценки — нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()



def request_gpt(system_prompt: str, user_prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return resp.choices[0].message.content


# ==== UI ====
st.title("CV Scoring App")

job_url = st.text_input("Ссылка на вакансию")
resume_url = st.text_input("Ссылка на резюме")

if st.button("Проанализировать соответствие"):
    if not job_url or not resume_url:
        st.warning("Введите обе ссылки: на вакансию и на резюме.")
    else:
        with st.spinner("Парсим данные и отправляем в GPT..."):
            try:
                job_html = get_html(job_url).text
                resume_html = get_html(resume_url).text

                job_text = extract_vacancy_data(job_html)
                resume_text = extract_resume_data(resume_html)

                prompt = f"# ВАКАНСИЯ\n{job_text}\n\n# РЕЗЮМЕ\n{resume_text}"
                answer = request_gpt(SYSTEM_PROMPT, prompt)

                st.subheader("📊 Результат анализа")
                st.markdown(answer)

                with st.expander("Показать распарсенные тексты"):
                    st.markdown("**Вакансия:**")
                    st.write(job_text)
                    st.markdown("**Резюме:**")
                    st.write(resume_text)

            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
