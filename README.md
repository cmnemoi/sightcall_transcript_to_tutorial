# SightCall Transcript to Tutorial

[![Continuous Integration](https://github.com/cmnemoi/sightcall_transcipt_to_tutorial/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/sightcall_transcipt_to_tutorial/actions/workflows/continuous_integration.yaml)
[![Continuous Delivery](https://github.com/cmnemoi/sightcall_transcipt_to_tutorial/actions/workflows/create_github_release.yaml/badge.svg)](https://github.com/cmnemoi/sightcall_transcipt_to_tutorial/actions/workflows/create_github_release.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/sightcall_transcipt_to_tutorial/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/sightcall_transcipt_to_tutorial)

An app to generate tutorials from SightCall support transcripts.

## Project Structure

- `backend/`: Contains the FastAPI backend application.
- `frontend/`: Contains the React frontend application.
- `docker/`: Contains Docker-related configurations (e.g., Dockerfiles for specific services if not in service directories, helper scripts).

# Installation

You need to have `curl` and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed on your system.

Then run the following command : `curl -sSL https://raw.githubusercontent.com/cmnemoi/sightcall_transcipt_to_tutorial/main/clone-and-install | bash`

## Local Development with Docker

This project uses Docker Compose to manage services for local development.

**Prerequisites:**
- Docker
- Docker Compose

**Setup:**
1. Clone the repository.
2. Environment variables will be managed via Docker Compose and `.env` files (e.g., `backend/.env`). Specific instructions for creating these will be part of the Docker setup tasks.
3. Run `docker-compose up --build` from the project root.

   - The backend will be available at `http://localhost:8000`.
   - The frontend will be available at `http://localhost:3000`.
   - The PostgreSQL database will be running and accessible to the backend.

# Development

Run tests with `make test`.

# License

The source code of this repository is licensed under the [AGPL-3.0-or-later License](LICENSE).