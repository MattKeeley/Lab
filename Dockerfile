# Base image
FROM python:3

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 4444

# Set environment variables
ENV MONGO_HOST mongodb
ENV MONGO_PORT 27017
ENV MONGO_DB challenge

# Run the application
CMD ["python3", "app.py"]