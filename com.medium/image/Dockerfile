FROM python:3-slim

# Tini
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# Dependencies
WORKDIR /opt/odf
COPY requirements.txt ./
RUN pip install -r requirements.txt

# App
COPY fetch.py ./

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "fetch.py"]
