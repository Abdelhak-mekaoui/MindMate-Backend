# Use the official Python image as the base image
# Use an official Python runtime as the base image with Python 3.10 or higher
FROM python:3.10

# Rest of your Dockerfile remains the same

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
