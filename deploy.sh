#!/bin/bash

export HEROKU_APP_NAME=media-generator

heroku container:push web --app $HEROKU_APP_NAME
heroku container:release web --app $HEROKU_APP_NAME
heroku open --app $HEROKU_APP_NAME
heroku logs --tail --app $HEROKU_APP_NAME
