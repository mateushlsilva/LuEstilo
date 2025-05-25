FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SENTRY_DSN=https://SENTRY_PUBLIC_KEY@SENTRY_HOST/SENTRY_PROJECT
ENV SQLALCHEMY_DATABASE_URL=postgresql://DB_USER:DB_PASSWORD@DB_HOST:5432/DB_NAME
ENV JWT_SECRET_KEY=YOUR_SECRET_KEY
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=60
ENV REFRESH_TOKEN_EXPIRE_DAYS=7
ENV TEST_EMAIL=admin@example.com
ENV TEST_SENHA=admin123


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]