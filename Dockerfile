from python:3

COPY taos /app/taos
COPY container.requirements.txt /app/

WORKDIR /app

RUN pip install -r container.requirements.txt
RUN pip install gunicorn


ENTRYPOINT ["python"]
CMD [ "-m", "taos.bot" ]
