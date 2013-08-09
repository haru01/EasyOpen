#!/bin/bash
ag --noheading --nobreak --nocolor $1 .easyopen_index | ag $2:[0-9]*:
