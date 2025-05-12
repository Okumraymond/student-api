FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Add user and set permissions
RUN useradd -m studentuser && \
    chown -R studentuser:studentuser /app

USER studentuser

# Ensure .local/bin is in PATH
ENV PATH="/home/studentuser/.local/bin:${PATH}"
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
