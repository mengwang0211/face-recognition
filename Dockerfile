FROM hzwangmeng/face_recognition:latest
RUN mkdir /code
COPY ./ /code

RUN pip install --upgrade pip -i https://pypi.douban.com/simple
RUN pip install face_recognition -i https://pypi.douban.com/simple
RUN pip install flask -i https://pypi.douban.com/simple
RUN pip install elasticsearch -i https://pypi.douban.com/simple

WORKDIR /code

CMD ["python","webserver.py"]



