FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt http.reqs.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt http.reqs.txt amqp.reqs.txt
COPY ./transaction.py ./invokes.py ./amqp_connection.py ./
CMD [ "python", "./transaction.py" ]
