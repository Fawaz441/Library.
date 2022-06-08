FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install pytz
RUN pip install -r requirements.txt 
COPY . .
# CMD [ "python", "manage.py", "create_admin" ]