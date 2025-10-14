# CV Scoring App (Streamlit)

Простое веб‑приложение на **Streamlit** для анализа соответствия кандидата вакансии с помощью моделей OpenAI.

> ⚠️ Проект использует секрет `OPENAI_API_KEY`. Локально он хранится в `.streamlit/secrets.toml`, а в Streamlit Cloud — задаётся в **App → Settings → Secrets**.

---

## ✨ Возможности
- Ввод ссылок на вакансию и резюме (hh.ru или другой источник).
- Парсинг страниц (см. `parse_hh.py`) и выделение ключевого текста.
- Запрос к OpenAI и генерация:
  - краткого анализа,
  - оценки качества оформления резюме,
  - итоговой оценки соответствия (1–10).
- UI с индикаторами загрузки и hot‑reload.

---

## 🏁 Быстрый старт (локально)

**Требования**: Python 3.10+, Git.

```powershell
# 1) Клонируем
git clone https://github.com/<your-username>/cv_scoring.git
cd cv_scoring

# 2) Виртуальная среда
python -m venv venv
.env\Scripts\Activate

# 3) Зависимости
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Секреты
mkdir .streamlit 2>$null
echo OPENAI_API_KEY=\"ВАШ_КЛЮЧ\" > .\.streamlit\secrets.toml

# 5) Запуск
streamlit run ".\streamlit_app.py"
```

После старта откройте ссылку из консоли, например `http://localhost:8501`.

> Если порт занят — добавьте `--server.port 8502`.

---

## 🔧 Конфигурация

### Секреты
- **Локально**: файл `.streamlit/secrets.toml`
  ```toml
  OPENAI_API_KEY = "ваш_реальный_ключ"
  ```
- **Streamlit Cloud**: App → Settings → Secrets:
  ```
  OPENAI_API_KEY = "ваш_реальный_ключ"
  ```

### Требуемые пакеты
Минимальный набор указан в `requirements.txt`. Если добавляете новые библиотеки — фиксируйте версии и проверяйте сборку в облаке.

---

## 🗂️ Структура проекта
```
cv_scoring/
├─ .streamlit/
│  └─ secrets.toml            # локальные секреты (НЕ коммитим)
├─ venv/                      # виртуальная среда (игнорируется)
├─ parse_hh.py                # функции парсинга страниц
├─ streamlit_app.py           # основное приложение Streamlit
├─ requirements.txt
└─ .gitignore
```

---

## ☁️ Деплой в Streamlit Cloud
1. Подключите репозиторий в Streamlit Community Cloud.
2. В настройках приложения укажите main‑файл: `streamlit_app.py`.
3. Задайте секрет `OPENAI_API_KEY` в **App → Settings → Secrets**.
4. Нажмите **Deploy** / **Rerun**.

---

## ▶️ Использование
1. Введите ссылку на **вакансию** и ссылку на **резюме**.
2. Нажмите **«Проанализировать соответствие»**.
3. Смотрите:
   - краткий анализ,
   - оценку качества резюме,
   - итоговый балл (1–10).

> Модуль `parse_hh.py` должен предоставлять функции:
> ```python
> get_html(url) -> requests.Response
> extract_vacancy_data(html: str) -> str
> extract_resume_data(html: str) -> str
> ```

---

## 🧩 Частые проблемы
- **`missing ScriptRunContext`** — запускаете как `python file.py`. Нужно:  
  `streamlit run streamlit_app.py`.
- **`StreamlitSecretNotFoundError`** — не найден `OPENAI_API_KEY`. Проверьте `.streamlit/secrets.toml` или секреты в облаке.
- **Ошибка сборки в Cloud** — проверьте `requirements.txt`. Уберите тяжёлые/OS‑специфичные пакеты и зафиксируйте версии.
- **Порт занят** — `streamlit run streamlit_app.py --server.port 8502`.

---

## 🗺️ Roadmap / Идеи
- Загрузка PDF/DOCX и извлечение текста в UI.
- Подсветка совпадений требований и навыков.
- Экспорт результатов (CSV/SQLite).
- Настройки модели и температуры в sidebar.
- Unit‑тесты для парсера.

---

## 🤝 Контрибьюции
PR и issue приветствуются. Перед PR — убедитесь, что билд проходит локально и в Cloud.

---

## 📄 Лицензия
MIT (при желании замените на свою).

---

## 🙌 Благодарности
- https://streamlit.io/
- https://github.com/openai/openai-python
