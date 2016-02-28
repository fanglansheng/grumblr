Platform: AWS EC2;

Database: MySQL;

Public DNS: ec2-52-27-40-196.us-west-2.compute.amazonaws.com

Config files in EC2:
1. /home/ubuntu/grumblr.wsgi
2. /etc/apache2/sites-available/grumblr.conf
3. /etc/apache2/apache2.conf : add this scentence at the end
    WSGIPythonPath /var/www/webapps


Other references:
1. how to deploy django:
(1)https://www.youtube.com/watch?v=hBMVVruB9Vs
Basically I followed this tutorial.

(2)https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04

2.permission problems I meet in EC2:
http://stackoverflow.com/questions/21797372/django-errno-13-permission-denied-var-www-media-animals-user-uploads

3.How to set environment variable:
https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps

4.How to set database:
https://dev.mysql.com/doc/refman/5.7/en/creating-database.html