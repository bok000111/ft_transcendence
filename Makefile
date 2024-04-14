NAME = ft_transcendence

COMPOSE_FILE = ./srcs/docker-compose.yml
DB_DIR = ./srcs/postgres_data/

all: $(NAME)

$(NAME): mkdir
	docker compose -f $(COMPOSE_FILE) up --build

clean:
	docker compose -f $(COMPOSE_FILE) down

fclean: clean
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	rm -rf $(DB_DIR)

re: fclean all

mkdir:
	mkdir -p $(DB_DIR)

.PHONY: all clean fclean re