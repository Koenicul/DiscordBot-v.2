FROM python:rc-buster
WORKDIR /app
COPY requirements.txt ./
RUN ["pip", "install", "--no-cache-dir" ,"-r", "requirements.txt"]
RUN ["python", "db.py"]
COPY . .
CMD [ "python", "bot.py"]