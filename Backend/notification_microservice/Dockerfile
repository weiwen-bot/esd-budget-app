FROM python:3-slim
WORKDIR /usr/src/app
COPY ./http.reqs.txt ./amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt -r http.reqs.txt
COPY ./notification.py ./
CMD [ "python", "./notification.py" ]

