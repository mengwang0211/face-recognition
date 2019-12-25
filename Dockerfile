FROM hzwangmeng/face_recognition:latest

MAINTAINER Meng Wang <wmlucas.cn@gmail.com>

RUN mkdir /code

COPY ./ /code

RUN pip install --upgrade pip -i https://pypi.douban.com/simple \
    && pip install face_recognition -i https://pypi.douban.com/simple \
    && pip install flask -i https://pypi.douban.com/simple \
    && pip install elasticsearch -i https://pypi.douban.com/simple

WORKDIR /code

CMD ["python","webserver.py"]




