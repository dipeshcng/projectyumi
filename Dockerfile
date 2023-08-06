FROM python:3.9-alpine


COPY requirements.txt requirements.txt
RUN  PYTHONPATH=/usr/bin/python pip install -r requirements.txt

COPY . yumi
WORKDIR /yumi

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]