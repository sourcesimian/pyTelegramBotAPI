test:
	trial tests/test_*.py


coverage:
	coverage run tests/test_types.py
	coverage html
	open htmlcov/index.html


develop:
	./setup_env.sh


clean:
	rm -rf build
	rm -rf _trial*
	rm -rf htmlcov


analyse:
	find TelegramBotAPI -name '*.py' | xargs pep8 --ignore E501
	find TelegramBotAPI -name '*.py' | xargs pyflakes
	find TelegramBotAPI -name '*.py' | xargs pylint -d invalid-name -d locally-disabled -d missing-docstring -d too-few-public-methods -d protected-access
