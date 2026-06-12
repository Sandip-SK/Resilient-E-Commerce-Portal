FROM python:3.9-slim

# create a non root user and group for security
RUN groupadd -r sreuser && useradd -r -g sreuser sreuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Change ownership of the app directory to the non-root user
RUN chown -R sreuser:sreuser /app

USER sreuser

EXPOSE 5000

CMD ["python", "app.py"]