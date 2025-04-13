FROM python:3.12-alpine

WORKDIR /app

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .

EXPOSE 8000

CMD [ "python", "main.py" ]