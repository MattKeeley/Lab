FROM python:3
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV MONGO_HOST mongodb
ENV MONGO_PORT 27017
ENV MONGO_DB challenge
CMD ["python3", "app.py"]