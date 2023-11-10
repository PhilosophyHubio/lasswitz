# lasswitz - Open Access Academic Editing Platform

Lasswitz, or Laßwitz, is an authoring tool for academic and scientific writings which looks to improve scientific and intellectual work through peer-to-peer exchanges. At the same time, it provides an open path for ANY person to interact, to suggest or to raise questions about the contents of each work.

## Getting Started (Docker)

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py.

  > cd lasswitz

- Assuming you installed and configured previously Docker, build a new image.

  > docker build -t "lasswitz" .

- Run your new image.

  > docker run -p 6543:6543 lasswitz

## Getting Started (standalone)

- Change directory into your newly created project if not already there. Your
  current directory should be the same as this README.txt file and setup.py.

  > cd lasswitz

- Create a Python virtual environment, if not already created.

  > python3 -m venv env

- Upgrade packaging tools, if necessary.

  > env/bin/pip install --upgrade pip setuptools

  - If you find, you don't have pip installed in your virtual environment, you can follow the instructions here: https://pip.pypa.io/en/stable/installation/

- Install the project in editable mode with its testing requirements.

   > env/bin/pip install -e ".[testing]"

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

    > env/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

    > env/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    > env/bin/initialize_lasswitz_db development.ini

- Run your project's tests.

    > env/bin/pytest

- Run your project.

    > env/bin/pserve development.ini
