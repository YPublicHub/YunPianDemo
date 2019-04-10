FROM python
COPY . /server/
WORKDIR /server
RUN pip install flask
RUN pip install gunicorn
RUN pip install PyMysql
EXPOSE 9992
CMD gunicorn -b 0.0.0.0:9992 -w 1 yp_callback:app

