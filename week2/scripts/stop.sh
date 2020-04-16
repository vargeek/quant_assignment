#!/bin/bash

ps aux | grep -v grep | grep quant | awk '{print $2}' | xargs kill -9
