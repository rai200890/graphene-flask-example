up:
	docker-compose run --service-ports --name user_api_flask_web web --rm

test:
	docker exec -it user_api_flask_web pytest tests

exec-db:
	docker exec -it user_api_flask_db bash

exec-web:
	docker exec -it user_api_flask_web bash
