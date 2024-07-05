NAME = ft_transcendence

MANAGE_PY = ./srcs/django/manage.py

all: $(NAME)

$(NAME):
	@echo "Everything must be launched with a single command line to run an autonomous container provided by Docker ."
	@echo "서브젝트에 이렇게 돼있어서 평가받을때는 Makefile 안쓰고 docker compose 직접 써야될수도 있음"
	@docker compose up --build

dev: mkdir
	docker compose up --build --watch

runserver:
	@${MANAGE_PY} makemigrations
	@${MANAGE_PY} migrate
	@${MANAGE_PY} runserver

down:
	docker compose down
clean:
	docker compose down --rmi all --remove-orphans
fclean:
	docker compose down --rmi all --remove-orphans --volumes
re: fclean all

.PHONY: all clean fclean re mkdir req freeze