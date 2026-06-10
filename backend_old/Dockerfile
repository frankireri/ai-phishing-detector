FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; [nltk.download(x, quiet=True) for x in ['stopwords','punkt','wordnet','punkt_tab']]"

COPY . .

RUN mkdir -p models_storage

ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_ENV=production

EXPOSE 5000

CMD ["sh", "-c", "python manage.py init-db && python manage.py train --dataset data/phishing_dataset.csv; gunicorn -w 2 -b 0.0.0.0:$PORT run:app"]
