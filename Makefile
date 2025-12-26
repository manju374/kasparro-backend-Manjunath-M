up:
	docker-compose up --build -d

down:
	docker-compose down

test:
	docker-compose run --rm backend pytest

logs:
	docker-compose logs -f backend
