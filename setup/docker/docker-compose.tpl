version: "3.6"
services:
  zillionare:
    build: .
    container_name: zillionare
    image: zillionare/zillionare:DEV_BUILD
    depends_on:
      - postgres
      - redis
    ports:
      - "3181:3181"
      - "3180:3180"
      - "8888:8888"
    
    working_dir: /apps
    environment:
      - __cfg4py_server_role__=PRODUCTION
      - INIT_BARS_MONTHS=13
      - JQ_ACCOUNT
      - JQ_PASSWORD
      - LANG=C.UTF-8
      - POSTGRES_USER=zillionare
      - POSTGRES_PASSWORD=123456
      - POSTGRES_DB=zillionare
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - TZ=Asia/Shanghai
  redis:
    image: redis:5.0.10-alpine
    container_name: redis
    restart: always
    expose: 
      - 6379
    command: sh -c 'redis-server --appendonly yes'
  postgres:
    image: postgres:10
    container_name: postgres
    restart: always
    expose: 
      - 5432
    environment:
      - POSTGRES_USER
      - POSTGRES_PASSWORD
      - POSTGRES_DB=zillionare
    volumes:
      - ./init/postgres:/docker-entrypoint-initdb.d
