FROM zauberzeug/nicegui:latest

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "main.py"]