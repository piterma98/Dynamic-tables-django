FROM python:3.11.9-slim

ENV USER proexe
ENV HOME /home/$USER
ENV PATH $HOME/.local/bin:$PATH
RUN useradd --user-group $USER --create-home --home-dir $HOME

USER $USER
WORKDIR $HOME

USER proexe


COPY ./app/requirements/base.txt /tmp/base.txt
RUN pip install --user --no-cache-dir -r /tmp/base.txt

WORKDIR $HOME/app
COPY ./app/ .

USER root
RUN ["chmod", "+x", "./entrypoint.sh"]
RUN mkdir -p static && chown -R proexe:proexe static
USER proexe

RUN pip install --user --no-cache-dir ipython==8.17.2
RUN python manage.py collectstatic --noinput


ENTRYPOINT [ "bash", "-c", "./entrypoint.sh" ]

