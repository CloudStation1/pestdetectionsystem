FROM python:bullseye

WORKDIR /usr/src/app

COPY notifier.requirements.txt ./
RUN pip install --no-cache-dir -r notifier.requirements.txt

COPY . .

CMD [ "python", "./notifier.py" ]