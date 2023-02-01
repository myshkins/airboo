#!/bin/bash

if [ $DEV_MODE == true ];then
    echo performing alembic migrations
    alembic upgrade head
fi

uvicorn main:app --host 0.0.0.0 --port 8100 --reload