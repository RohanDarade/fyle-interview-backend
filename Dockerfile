# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=core.server.py
ENV FLASK_ENV=development

# Run the script when the container launches
CMD ["gunicorn", "-w", "4", "-k", "gevent", "core.server:app", "--bind", "0.0.0.0:8000", "--reload"]