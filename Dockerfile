
FROM python:3.10-slim-bookworm

# Set environment variables.
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ARG GOOGLE_CLIENT_ID
ENV GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID

ARG GOOGLE_CLIENT_SECRET
ENV GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

ARG SECRET
ENV SECRET=$SECRET

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips=*"]