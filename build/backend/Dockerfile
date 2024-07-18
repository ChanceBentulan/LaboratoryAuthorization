# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements file to leverage Docker cache
COPY ../../backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application files
COPY ../../backend .

# Install psycopg2 for PostgreSQL support
RUN pip install psycopg2-binary

# Make the entrypoint script executable
RUN chmod +x /app/wait-for-psql.sh

# Make port 80 available to the world outside this container
EXPOSE 5000

ENTRYPOINT ["/app/wait-for-psql.sh"]

# Run app.py when the container launches
CMD ["python", "app.py", "0:5000"]