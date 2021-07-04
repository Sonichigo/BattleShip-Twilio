FROM python:3.6
WORKDIR /
RUN pip install flask
RUN pip install twilio
COPY server.py .
COPY battleship.py .
ENTRYPOINT ["python", "server.py"]