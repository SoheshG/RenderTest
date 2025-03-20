# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose the port your Flask app runs on
EXPOSE 10000

# Start the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
