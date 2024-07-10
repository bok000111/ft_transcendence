NAME = ft_transcendence

all: $(NAME)

$(NAME):
	docker compose up --build
dev:
	docker compose up --build --watch
down:
	docker compose down
clean:
	docker compose down --rmi all --remove-orphans
fclean:
	docker compose down --rmi all --remove-orphans --volumes
	docker system prune -a
re: fclean all

.PHONY: all clean fclean re down