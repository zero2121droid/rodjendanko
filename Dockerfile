FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install drf-yasg==1.20.0
#RUN pip install --upgrade pip setuptools

COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=rodjendanko_backend.settings

EXPOSE 8000

# Run the Django development server
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
RUN mkdir -p /app/media
ENTRYPOINT ["/app/entrypoint.sh"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "rodjendanko_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

