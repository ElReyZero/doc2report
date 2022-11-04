FROM ubuntu:22.04

RUN apt update && apt dist-upgrade -y && apt install -y python3 python3-pip git

COPY accounts /home/doc2report/accounts
COPY docs2report /home/doc2report/docs2report
COPY documents /home/doc2report/documents
COPY reports /home/doc2report/reports
COPY static /home/doc2report/static
COPY templates /home/doc2report/templates
COPY config.py /home/doc2report/config.py
COPY config.cfg /home/doc2report/config.cfg
COPY requirements.txt /home/doc2report/requirements.txt
COPY manage.py /home/doc2report/manage.py
RUN pip3 install -r /home/doc2report/requirements.txt
RUN python3.10 /home/doc2report/manage.py migrate
ENTRYPOINT python3.10 /home/doc2report/manage.py runserver