Push Notification microservice
subcribes to a rabbitMQ broker, reads messages from there and sends them off to APN (add the android one later)

doesn't deal in payload business logic, all this does is take messages from the queue and forward them to the appropriate notification service

TODO: batching requests to APNs
TODO: the python listener sometimes starts before the rabbitmq server is up, crashing