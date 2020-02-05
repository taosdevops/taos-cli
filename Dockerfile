from python:3

WORKDIR /app

COPY container.requirements.txt /app/
RUN pip install -r requirements.txt

COPY taos /app/taos

ENTRYPOINT ["python"]
CMD [ "-m", "taos.bot" ]
