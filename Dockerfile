FROM python:3.9-slim

WORKDIR /app

# Copy the application files to the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8501



ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]