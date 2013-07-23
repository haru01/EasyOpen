#!/bin/bash
ag -G $1 --noheading --nobreak --nocolor --line-numbers $2 .  > .easyopen_index
