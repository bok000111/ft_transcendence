NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = /goinfre/$(USER)/postgres_data

VENV_DIR = /goinfre/$(USER)/venv
REQUIREMENTS = ./srcs/requirements.txt

all: $(NAME)

$(NAME): mkdir venv
	docker compose -f $(COMPOSE_FILE) up --build -d

	@echo run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment
	@echo run 'deactivate' to deactivate the virtual environment
	@echo run 'pip freeze > $(REQUIREMENTS)' to update the requirements.txt file
	@echo run 'python -m venv --clear $(VENV_DIR)' to clear the virtual environment
	@echo run 'python manage.py makemigrations' to make migrations
	@echo run 'python manage.py migrate' to apply migrations
	@echo run 'python manage.py runserver' to start the server

venv:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

clean:
	docker compose -f $(COMPOSE_FILE) down

fclean: clean
	docker system prune -a -f
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	rm -rf $(DB_DIR) $(VENV_DIR)

re: fclean all

mkdir:
	mkdir -p $(DB_DIR)

.PHONY: all clean fclean re mkdir venv