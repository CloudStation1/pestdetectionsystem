FROM python:bullseye

WORKDIR /usr/src/app

COPY webapp.requirements.txt ./
RUN pip install --no-cache-dir -r webapp.requirements.txt

COPY . .

CMD [ "python", "./main.py" ]