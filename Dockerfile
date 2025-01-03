# Use the official Python 3.10 image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your application's requirements.txt to the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "src/app.py"]
