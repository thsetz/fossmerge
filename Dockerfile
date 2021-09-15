FROM python:3.9-slim
RUN apt-get update && apt-get upgrade && apt-get install -y \
pandoc  \
python3-lxml  \
vim  \
build-essential

RUN pip3 install poetry 

# poetry install 
        

