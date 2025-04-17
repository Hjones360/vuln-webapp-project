# Use the official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy your local files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
