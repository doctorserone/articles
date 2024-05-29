FROM python:3.12.2-bookworm

# Install cron service
RUN apt-get update && apt-get -y install cron vim

# set some environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Execute cron service after migration
RUN mkdir /cron
RUN touch /cron/movements.log
RUN service cron restart

# copy project
COPY ./app/src/ticmagicalline .

ENTRYPOINT [ "/entrypoint.sh" ]
