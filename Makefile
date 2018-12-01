#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

init:
	pip install -r requirements.txt

bandit:
	bandit -r hocke.py hockepy tests

pycodestyle:
	pycodestyle --exclude=venv --filename="*.py" .

pylint:
	pylint --reports=n hocke.py hockepy tests

pylint-error:
	pylint --reports=n --disable=C,R,W hocke.py hockepy tests

test:
	python -m unittest discover -v tests

travis: bandit pycodestyle pylint-error test

