FROM python:3.10
COPY app /app
RUN pip install -r /app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
