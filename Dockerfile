# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port on which the Flask app will run
EXPOSE 5000

# Step 6: Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Step 7: Run the Flask app
CMD ["flask", "run"]
