############################################################
# Dockerfile to build Docker-Todo NGinx
#
# Build with: IMAGE=$(docker build -q . | egrep -o "\w+$"); for v in latest 1.10.2 1.10 1; do docker tag $IMAGE brianmorgan/nginx:$v; done
#
# To push: for v in latest 1.10.1 1.10 1; do docker push brianmorgan/nginx:$v; done
############################################################

FROM ubuntu:xenial

MAINTAINER Docker Todo "docker-todo@gocatalant.com"

ENV NGINX_VERSION 1.10.2*

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/ubuntu/ xenial nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install --no-install-recommends --no-install-suggests -y \
						ca-certificates \
						nginx="$NGINX_VERSION" \
						nginx-module-xslt \
						nginx-module-geoip \
						nginx-module-image-filter \
						nginx-module-perl \
						nginx-module-njs \
						gettext-base \
	&& rm -rf /var/lib/apt/lists/*

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

# Remove the default site
RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 80 443

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
