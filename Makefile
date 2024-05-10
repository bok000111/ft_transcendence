NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = /goinfre/$(USER)/postgres_data
REQUIREMENTS = ./srcs/requirements.txt
MANAGE_PY = ./srcs/requirements/django/manage.py
TESTS = ./srcs/requirements/django

all: $(NAME)

$(NAME): mkdir
	docker compose -f $(COMPOSE_FILE) up --build -d
	
	@echo "run \"manage makemigrations\" to make migrations"
	@echo "run \"manage migrate\" to apply migrations"
	@echo "run \"manage runserver\" to start the server"

clean:
	docker compose -f $(COMPOSE_FILE) down

fclean: clean
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker system prune -af --volumes
	sudo rm -rf $(DB_DIR)

re: fclean all

mkdir:
	sudo mkdir -p $(DB_DIR)

req:
	pip install -r $(REQUIREMENTS) --user -q --no-cache-dir

freeze:
	pip freeze > $(REQUIREMENTS)

dev: mkdir
	docker compose -f $(COMPOSE_FILE) up --build -d --scale redis=0

dbc:
	docker exec -it postgres psql -U postgres -c "DROP DATABASE ft_transcendence;"
	docker exec -it postgres psql -U postgres -c "CREATE DATABASE ft_transcendence;"

test:
	$(MANAGE_PY) test $(TESTS) --parallel

.PHONY: all clean fclean re mkdir req freeze dev dbc test