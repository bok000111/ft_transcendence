NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = /goinfre/$(USER)/postgres_data
REQUIREMENTS = ./srcs/requirements.txt
MANAGE_PY = ./srcs/requirements/django/manage.py
TESTS = ./srcs/requirements/django

all: $(NAME)

$(NAME): mkdir req containers migrate
	@echo "run \"manage makemigrations\" to make migrations"
	@echo "run \"manage migrate\" to apply migrations"
	@echo "run \"manage runserver\" to start the server"

	@${MANAGE_PY} runserver

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

containers:
	docker compose -f $(COMPOSE_FILE) up --build -d --wait

migrate:
	@${MANAGE_PY} makemigrations && ${MANAGE_PY} migrate

freeze:
	pip freeze > $(REQUIREMENTS)

dev: mkdir
	docker compose -f $(COMPOSE_FILE) up --build -d --scale redis=0


dbc:
	@${MANAGE_PY} flush --no-input

test:
	$(MANAGE_PY) test $(TESTS) --parallel

lint:
	pylint --rcfile=./srcs/.pylintrc $(TESTS)/*

.PHONY: all clean fclean re mkdir req containers migrate freeze dev dbc test lint