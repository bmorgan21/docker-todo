FROM brianmorgan/nginx:latest

ENV CODE_DIR /www/data

RUN mkdir -p ${CODE_DIR}
WORKDIR ${CODE_DIR}

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sL https://deb.nodesource.com/setup_7.x | bash - \
    && apt-get install -y --no-install-recommends build-essential nodejs

ADD package.json bower.json ${CODE_DIR}/
RUN npm install

ADD . ${CODE_DIR}

ENV STATIC_ROOT_DIR="$CODE_DIR/app"
RUN mkdir /docker-entrypoint-init-nginx.d
COPY docker-config-init.sh /docker-entrypoint-init-nginx.d/docker-config-init.sh
