# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run Uvicorn with Gunicorn when the container launches
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:80"]
