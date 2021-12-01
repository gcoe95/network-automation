FROM ubuntu:20.04

MAINTAINER George Coe

SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-dev python3-pip
RUN pip install Flask behave jinja2 requests ncclient netmiko

RUN source /etc/apache2/envvars
RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf
RUN a2dissite 000-default
RUN a2dissite default-ssl
RUN a2enmod wsgi

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOG_DIR /var/log/apache2

COPY src /var/www/src

COPY src/flask.conf /etc/apache2/sites-available/flask.conf
RUN chown -R www-data:www-data /var/www/src
RUN chown www-data:www-data /etc/apache2/sites-available/flask.conf
RUN a2ensite flask.conf

EXPOSE 8080
CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]