FROM apache/airflow:2.9.2

USER root
RUN apt-get update
RUN apt install -y default-jdk
RUN apt-get autoremove -yqq --purge
RUN apt-get install -y wget
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Install JDK
RUN wget https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.tar.gz && \
    mkdir -p /opt/java && \
    tar -xvf jdk-22_linux-x64_bin.tar.gz -C /opt/java && \
    rm jdk-22_linux-x64_bin.tar.gz

# Install JAVA
RUN wget -O jre-8u421-linux-x64.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=250118_d8aa705069af427f9b83e66b34f5e380 && \
    tar -xvf jre-8u421-linux-x64.tar.gz -C /opt/java && \
    rm jre-8u421-linux-x64.tar.gz

# Install Apache Spark
RUN wget https://downloads.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz && \
    mkdir -p /opt/spark && \
    tar -xvf spark-3.5.3-bin-hadoop3.tgz -C /opt/spark && \
    rm spark-3.5.3-bin-hadoop3.tgz

# Download the JDBC driver for PostgreSQL and move it to the jars folder
RUN wget https://jdbc.postgresql.org/download/postgresql-42.7.4.jar && \
    mv postgresql-42.7.4.jar /opt/spark/spark-3.5.3-bin-hadoop3/jars


# Setting environment variables
# ENV JAVA_HOME=/opt/java/jdk-22.0.2
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV SPARK_HOME=/opt/spark/spark-3.5.3-bin-hadoop3
ENV PATH=$PATH:$JAVA_HOME/bin
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip

# Installing the rest of the packages via pip
COPY requirements.txt /requirements.txt
RUN chmod 777 /requirements.txt

USER airflow
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt