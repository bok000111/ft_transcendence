NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = /goinfre/$(USER)/postgres_data
REQUIREMENTS = /workspaces/ft_transcendence/srcs/requirements.txt
MANAGE_PY = /workspaces/ft_transcendence/srcs/manage.py

all: $(NAME)

$(NAME): mkdir
	docker compose -f $(COMPOSE_FILE) up --build -d
	
	@pip install -r $(REQUIREMENTS) --user -q
	@echo "run \"echo alias manage=\"python /workspaces/ft_transcendence/srcs/requirements/django/manage.py\" >> /home/vscode/.zshrc/ to add manage.py alias\""
	@echo "일단은 이렇게 해놓고 나중에 수정, alias 설정해야 편함"
	@echo
	@echo "run \"'pip install -r $(REQUIREMENTS)'\"		to install the requirements"
	@echo "run \"'pip freeze > $(REQUIREMENTS)'\"			to update the requirements.txt file"
	@echo
	@echo "run \"manage makemigrations\"								to make migrations"
	@echo "run \"manage migrate\"									to apply migrations"
	@echo "run \"manage runserver\"									to start the server"

clean:
	docker compose -f $(COMPOSE_FILE) down

fclean: clean
	docker system prune -a
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	sudo rm -rf $(DB_DIR)

re: fclean all

mkdir:
	sudo mkdir -p $(DB_DIR)

.PHONY: all clean fclean re mkdir venv