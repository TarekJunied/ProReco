sudo chcon -Rt httpd_sys_content_t /var/www/proreco.co

sudo systemctl restart nginx