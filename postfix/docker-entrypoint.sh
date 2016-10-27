#!/bin/ash
set -eo pipefail

# if command starts with an option, prepend postfix
if [ "${1:0:1}" = '-' ]; then
	set -- postfix "$@"
fi

if [ "$1" = 'postfix' -a "$(id -u)" = '0' ]; then

    if [ ! -f "/tmp/postfix_first_run" ]; then

        # Touch
        touch /var/log/mail.log /var/log/mail.err /var/log/mail.warn
        chmod a+rw /var/log/mail.*

        # Install supervisor script
        mkdir -p /etc/supervisor/conf.d
        cat > /etc/supervisor/conf.d/supervisord.conf <<EOF
[supervisord]
nodaemon=true
[program:postfix]
command=/opt/postfix.sh
[program:rsyslog]
command=/usr/sbin/rsyslogd -n
EOF

        # Install postfix script
        mkdir -p /opt
        cat >> /opt/postfix.sh <<EOF
#!/bin/ash
postfix start
tail -F /var/log/mail.*
EOF

       chmod +x /opt/postfix.sh

       # Configure main.cf
       sed -i -e "s/\$SMTP_SASL_PASSWORD_MAPS/$POSTFIX_PASSWORD_MAP/g" /etc/postfix/main.cf
       sed -i -e "s/\$RELAY_HOST/$POSTFIX_RELAY_HOST/g" /etc/postfix/main.cf

    fi

    set -- /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

fi

exec "$@"
