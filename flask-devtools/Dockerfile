FROM brianmorgan/flask:latest

RUN apt-get install -y --no-install-recommends mysql-client wget software-properties-common \
    && add-apt-repository -y ppa:webupd8team/java \
    && apt-get update \
    && echo "oracle-java6-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections \
    && echo "oracle-java6-installer shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections \
    && apt-get install -y --no-install-recommends oracle-java6-installer \
    && wget https://s3.amazonaws.com/com.hourlynerd.files/mysql-diff-0.3.tar.gz \
    && tar -xzvf mysql-diff-0.3.tar.gz -C /opt/ \
    && rm -rf mysql-diff-0.3.tar.gz
