# set base image (host OS)
FROM python:3.11

# set the working directory in the container
WORKDIR /app

COPY . .

RUN pip install -e ".[testing]"
RUN alembic -c docker.ini revision --autogenerate -m "init"
RUN alembic -c docker.ini upgrade head
RUN initialize_lasswitz_db docker.ini

EXPOSE 6543

CMD [ "pserve", "docker.ini" ]