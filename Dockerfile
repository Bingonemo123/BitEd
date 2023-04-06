FROM python:3.11.2

RUN pip install --upgrade pip

# ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
# EXPOSE 8000

# CMD ["python", "manage.py", "runserver"]
