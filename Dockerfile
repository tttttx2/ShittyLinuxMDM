FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV DOC_PROJECT_URL="https://github.com/tttttx2/ShittyLinuxMDM"
ENV DOC_PROJECT_NAME="ShittyLinuxMDM"
ENV DOC_PROJECT_LICENSE="UNDEFINED"

COPY app /app/

CMD [ "python3", "/app/main.py"]
