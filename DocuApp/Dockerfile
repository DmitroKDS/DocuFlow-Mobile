FROM python:3.10-slim

WORKDIR /app

COPY ./DocuApp .

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r /app/requirements.txt


CMD ["gunicorn", "gateway:docu_flow_app", "-b", "0.0.0.0:5000", "-w", "4"]

