# air-quality
to start:
`$ docker compose --profile full up --build`

to auto-generate alembic migration (with containers running)
`$ docker exec -u 1000 air_api alembic revision --autogenerate -m 'message'`

to manually run alembic migrations:
`$ docker exec -u 1000 air_api alembic upgrade head` (will upgrade to latest)

`$ docker exec -u 1000 air_api alembic upgrade <revision>` (will upgrade to specific revision)

`$ docker exec -u 1000 air_api alembic downgrade base` (will downgrade to empty database)

`$ docker exec -u 1000 air_api alembic downgrade <revision>` (will downgrade to specific revision)