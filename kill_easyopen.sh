#!/bin/bash

ps aux | grep EasyOpen | grep -v grep | awk '{print $2}' | xargs kill
