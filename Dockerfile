FROM python:rc-buster
WORKDIR /app
COPY requirements.txt ./
RUN ["pip", "install", "--no-cache-dir" ,"-r", "requirements.txt"]
COPY . .
CMD ["bash", "-c", "python3 db.py && python3 bot.py"]