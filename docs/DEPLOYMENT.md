# Deployment

## Local Docker

```bash
docker compose up --build
```

Services:

- Web: `http://localhost:3000`
- API: `http://localhost:8000/api/health`
- Postgres: `localhost:5432`

## Production Checklist

- Set `JWT_SECRET` to a strong secret.
- Configure `DATABASE_URL` for managed PostgreSQL.
- Configure CORS to the production web origin.
- Add market data and news provider API keys.
- Configure OpenAI or Anthropic credentials.
- Configure Gmail OAuth refresh token or SendGrid.
- Run behind HTTPS with rate limiting.
- Add observability export for logs, traces, and scheduler failures.
- Add compliance disclaimers and avoid presenting output as guaranteed financial advice.

## Daily Report Schedule

The API scheduler creates a cron job at `DAILY_REPORT_HOUR_SGT`, default `7`, in `Asia/Singapore`.

Production behavior should:

1. Fetch opted-in users.
2. Generate personalized reports from holdings and watchlists.
3. Send via Gmail API or SendGrid.
4. Store the generated report and delivery status.
5. Write audit events.
