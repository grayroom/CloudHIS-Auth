FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV MARIA_AUTH_NAME=his_auth
ENV MARIA_AUTH_USER=jeonghoon
ENV MARIA_AUTH_PW=@flatron23
ENV MARIA_PORT=3306

RUN JWT_PRIVATE_KEY=$(cat /etc/secret/private.pem) && \
    JWT_PUBLIC_KEY=$(cat /etc/secret/public.pem) &&
# RUN export JWT_PRIVATE_KEY && \
#     export JWT_PUBLIC_KEY

CMD ["python3", "manage.py", "runserver", "0:8000"]

EXPOSE 8000
