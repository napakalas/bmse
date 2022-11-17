start:
	docker compose up -d

start-build:
	docker compose up -d --build

start-build-recreate:
	docker compose up -d --build --force-recreate

stop:
	docker compose down

log-app:
	docker compose logs -f app

log-proxy:
	docker compose logs -f nginx

log-frontend:
	docker compose logs -f frontend
	
start-remote:
	docker context create --docker host=ssh://ubuntu@$(ip) remote_bmse	\
	docker context use remote_bmse	\
	docker compose --context remote_bmse build	\
	docker compose --context remote_bmse up -d