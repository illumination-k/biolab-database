# 手順

## migration

```bash
docker-compose up -d
docker-compose exec api bash
(app)$ alembic revision --autogenerate -m "create User table"
(app)$ alembic upgrade head
```