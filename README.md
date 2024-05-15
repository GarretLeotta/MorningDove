Push Notification microservice
subcribes to a rabbitMQ broker, reads messages from there and sends them off to APN (add the android one later)

TODO: the python listener sometimes starts before the rabbitmq server is up, crashing