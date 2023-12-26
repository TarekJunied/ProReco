# gunicorn_config.py

import multiprocessing

bind = "0.0.0.0:8000"  # Replace with the IP and port you want Gunicorn to bind to
workers = 5
certfile = '/etc/letsencrypt/live/proreco.co/cert.pem'  # Path to your SSL/TLS certificate file
keyfile = '/etc/letsencrypt/live/proreco.co/privkey.pem '  # Path to your SSL/TLS private key file
