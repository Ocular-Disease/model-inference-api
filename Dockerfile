FROM  python:3.7-alpine

WORKDIR /app

LABEL maintainer="Mohamed Belkamel"

# Install dependencies
RUN apk add --no-cache python3-pip
RUN pip3 install -r requirements.txt

COPY . /app


CMD ["uvicorn", "app:app",  "--host=0.0.0.0",  "--port=${PORT:-5000}"]