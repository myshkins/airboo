#!/bin/bash

if [[ $DO_MIGRATIONS == 1 ]];
then
    echo DO_MIGRATIONS = $DO_MIGRATIONS 
    echo performing alembic migrations
    alembic upgrade head
fi

if [[ $DEV_MODE == 1 ]];
then
    echo DEV_MODE = $DEV_MODE
    uvicorn main:app --host 0.0.0.0 --port 10100 --reload
else
    uvicorn main:app --host 0.0.0.0 --port 10100
fi
