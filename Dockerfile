FROM python:3.10-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Загрузка ресурсов NLTK
RUN python -c "import nltk; nltk.download('punkt')"

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
