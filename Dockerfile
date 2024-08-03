FROM denoland/deno:1.45.5

WORKDIR /app

COPY index.html ./
COPY img ./img
COPY server.ts ./

EXPOSE 8080

CMD ["run", "--allow-net", "--allow-write", "--allow-read", "server.ts"]