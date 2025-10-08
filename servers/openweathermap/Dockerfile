FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Expose port
EXPOSE 8000

# Run the FastMCP server
CMD ["python", "-m", "fastmcp", "run", "server.py", "--transport", "streamable-http", "--port", "8000"]
