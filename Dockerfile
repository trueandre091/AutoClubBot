ARG PYTHON_VERSION=3.11.8
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY src/requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code into the container.
COPY . .
RUN python src/DB/database.py

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python src/main.py
