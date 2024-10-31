FROM debian:stable
ENV URL=https://tablab.io/checker

# Update the repository sources list
RUN apt-get update

# Install and run apache
RUN apt-get install -y apache2 && apt-get clean
RUN a2enmod headers # Enables the mod_headers module
COPY ./ports.conf /etc/apache2/ports.conf

# Copy the HTML code
RUN rm /var/www/html/index.html
RUN mkdir /var/www/html/0
COPY ./index.html /var/www/html/0/index.html

EXPOSE 8080
ENTRYPOINT exec apachectl -D FOREGROUND

