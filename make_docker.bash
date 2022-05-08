#!/bin/bash

docker build -t sheng-bot . && docker run -itd --name sheng-bot sheng-bot
