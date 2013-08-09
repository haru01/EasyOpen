#!/bin/bash
ag -G rb --noheading --nobreak --nocolor --line-numbers $1 . | grep -v \.js:[0-9]*: >> .easyopen_index
ag -G rb --noheading --nobreak --nocolor --line-numbers $1  `bundle list --paths` | grep -v \.js:[0-9]*: >> .easyopen_index
