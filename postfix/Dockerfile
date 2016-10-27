############################################################
# Dockerfile to build CT postfix containers
# Based on Alpine 3.4
#
# Build with: IMAGE=$(docker build -q . | egrep -o "\w+$") && for v in latest 3.1.1 3.1 3; do docker tag $IMAGE catalant/postfix:$v; done
#
# To push: for v in latest 3.1.1 3.1 3; do docker push catalant/postfix:$v; done
############################################################

FROM alpine:3.4

RUN apk add --no-cache postfix rsyslog supervisor
EXPOSE 25

COPY config/main.cf /etc/postfix/main.cf

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["postfix"]
