#!/bin/bash

echo JWT_SECRET_POMPEEVA=$JWT_SECRET_POMPEEVA >> .env
echo JWT_EXPIRATION_TIME_POMPEEVA=$JWT_EXPIRATION_TIME_POMPEEVA >> .env

echo KAFKA_BOOTSTRAP_SERVERS_POMPEEVA=$KAFKA_BOOTSTRAP_SERVERS_POMPEEVA >> .env
echo TOPIC_POMPEEVA=$TOPIC_POMPEEVA >> .env

echo DB_HOST_POMPEEVA=$DB_HOST_POMPEEVA >> .env
echo DB_PORT_POMPEEVA=$DB_PORT_POMPEEVA >> .env
echo DB_NAME_POMPEEVA=$DB_NAME_POMPEEVA >> .env
echo DB_USER_POMPEEVA=$DB_USER_POMPEEVA >> .env
echo DB_PASS_POMPEEVA=$DB_PASS_POMPEEVA >> .env


