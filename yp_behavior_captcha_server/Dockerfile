FROM python
COPY . /server/
WORKDIR /server
RUN pip install flask
RUN pip install gunicorn
RUN pip install requests
RUN pip install pyyaml
EXPOSE 9996
CMD gunicorn -b 0.0.0.0:9996 -w 1 server:app
