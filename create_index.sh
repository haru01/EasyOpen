#!/bin/bash
rm .easyopen_index

ag -G $1 --noheading --nobreak --nocolor --line-numbers $2 . > .easyopen_index
ag -G $1 --noheading --nobreak --nocolor --line-numbers $2  `bundle list --paths` >> .easyopen_index
