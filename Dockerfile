FROM denoland/deno:1.45.5

WORKDIR /app

COPY src/ /app/
COPY assets/ /app/assets/

RUN mkdir -p /app/downloads && chmod 777 /app/downloads

EXPOSE 8080

CMD ["deno", "run", "--allow-net", "--allow-write", "--allow-env", "--allow-read", "--allow-run", "main.ts"]