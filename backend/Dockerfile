FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

# Create a non-root user with UID and GID 1000
RUN addgroup --gid 1000 appuser \
    && adduser --uid 1000 --gid 1000 --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "sightcall_transcript_to_tutorial.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]