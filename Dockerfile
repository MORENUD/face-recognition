FROM python:3.9-slim

# 1. Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2. Install System Dependencies (OpenCV requires these)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# 3. Handle Weights Directory (Fixes permission issues)
RUN mkdir -p /code/weights
ENV DEEPFACE_HOME="/code/weights"

# 4. Copy and Install Requirements
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy the App
COPY ./app /code/app

# 6. Add App to Python Path
ENV PYTHONPATH="${PYTHONPATH}:/code/app"

# 7. Run Command
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-80}"]