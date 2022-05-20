FROM  python:3.8

LABEL maintainer="Mohamed Belkamel"


RUN apt-get update && apt-get install -y python3-pip


RUN pip3 install -r requirements.txt


CMD ["python", "-m", "uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]