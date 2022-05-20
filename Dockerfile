FROM  python:3.8
LABEL maintainer="Mohamed Belkamel"

WORKDIR /app

COPY . .


RUN pip install --no-cache-dir --upgrade -r requirements.txt


CMD ["python", "-m", "uvicorn", "app:app",  "--host=0.0.0.0",  "--port" "5000"]