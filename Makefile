first_start: # Начальная инициализация
	@echo "--- First start! ---"
	sudo poetry shell
	poetry install
	@echo "--- Complete! ---"

pre-commit: # Проверки pre-commit
	@echo "--- pre-commit start! ---"
	pre-commit run --all-files

up: # Запустить env
	sudo poetry shell
	@echo "--- env started! ---"

down: # Выйти из env
	exit
	@echo "--- env exited! ---"
