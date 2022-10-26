start:
	docker-compose up -d

start-build:
	docker-compose up -d --build

start-build-recreate:
	docker-compose up -d --build --force-recreate

stop:
	docker-compose down

log-backend:
	docker logs -f casbert-ir_app_1

log-proxy:
	docker logs -f casbert-ir_nginx_1

log-frontend:
	docker logs -f casbert-ir_frontend_1

restart-backend:
	docker-compose restart app
