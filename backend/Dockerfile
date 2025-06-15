FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

COPY pyproject.toml README.md /app/

RUN pip install --no-cache-dir .

COPY ./sightcall_transcript_to_tutorial /app/sightcall_transcript_to_tutorial

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "sightcall_transcript_to_tutorial.main:app", "--host", "0.0.0.0", "--port", "8000"]
