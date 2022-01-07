from python:latest

RUN adduser  ctf

COPY ./app /app 

COPY flag.txt /flag 

RUN chmod 775 -R /app/*
ENV PORT 8888 
USER ctf

CMD ["/usr/local/bin/python","/app/main.py"]
