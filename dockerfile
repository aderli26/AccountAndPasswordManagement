# 
FROM python:3.8

# 
WORKDIR /app

# 
COPY . /app

# 
RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

RUN python db_setup.py

# 
CMD ["gunicorn", "-c","config.py"]