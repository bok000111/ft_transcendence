NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = /goinfre/$(USER)/postgres_data
STATIC_DIR = /goinfre/$(USER)/static_data
REQUIREMENTS = ./srcs/requirements/django/requirements.txt
MANAGE_PY = ./srcs/requirements/django/manage.py

all: $(NAME)

$(NAME): mkdir
	docker compose -f $(COMPOSE_FILE) up --build

dev: mkdir
	docker compose -f $(COMPOSE_FILE) up --build -d --scale django=0 --wait
	@${MANAGE_PY} makemigrations
	@${MANAGE_PY} migrate
	@${MANAGE_PY} runserver

down:
	docker compose -f $(COMPOSE_FILE) down

clean: down
fclean: clean
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker system prune -af --volumes
	sudo rm -rf $(DB_DIR) $(STATIC_DIR)

re: fclean all

mkdir:
	mkdir -p $(DB_DIR) $(STATIC_DIR)

req:
	pip install -r $(REQUIREMENTS) --user -q --no-cache-dir

freeze:
	pip freeze > $(REQUIREMENTS)

lint:
	pylint --rcfile=./srcs/.pylintrc ./srcs/requirements/django/*/*.py
	
.PHONY: all clean fclean re mkdir req freeze