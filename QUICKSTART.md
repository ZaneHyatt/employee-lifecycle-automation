# Quickstart

## 1. Clone the repo

git clone <repo-url>
cd employee-lifecycle-automation

## 2. Create .env

cp .env.example .env

# Fill in required values

## 3. Run with Docker

docker compose build
docker compose run --rm employee-lifecycle-automation

## 4. (Optional) Set up cron

0 6 \* \* \* cd /path/to/repo && docker compose run --rm employee-lifecycle-automation >> cron.log 2>&1
