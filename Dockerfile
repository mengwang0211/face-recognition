FROM hzwangmeng/face_recognition:latest

MAINTAINER Meng Wang <wmlucas.cn@gmail.com>

RUN mkdir /code \
    && mkdir -p /var/log/gunicorn

COPY ./ /code

RUN pip install --upgrade pip -i https://pypi.douban.com/simple \
    && pip install face_recognition -i https://pypi.douban.com/simple \
    && pip install flask -i https://pypi.douban.com/simple \
    && pip install elasticsearch -i https://pypi.douban.com/simple \
    && pip install --no-cache-dir gunicorn -i https://pypi.douban.com/simple

WORKDIR /code

ENV PORT 8000
EXPOSE 8000 5000

CMD ["/usr/local/bin/gunicorn", "-w", "2","--log-level","debug","--log-file","./logs/api.log","-b", ":8000", "webserver:app"]




