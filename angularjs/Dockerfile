FROM brianmorgan/nginx:latest

ENV CODE_DIR /www/data

RUN mkdir -p ${CODE_DIR}
WORKDIR ${CODE_DIR}

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git \
    && curl -sL https://deb.nodesource.com/setup_7.x | bash - \
    && apt-get install -y --no-install-recommends build-essential nodejs

RUN echo '{ "allow_root": true }' > /root/.bowerrc

ADD package.json bower.json ${CODE_DIR}/
RUN npm install --unsafe-perm

ADD ./app ${CODE_DIR}/app

ENV ANGULARJS_ROOT_DIR="$CODE_DIR"
RUN mkdir /docker-entrypoint-init-nginx.d
COPY docker-config-init.sh /docker-entrypoint-init-nginx.d/docker-config-init.sh
