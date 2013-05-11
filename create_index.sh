#!/bin/bash
rm .easyopen_index

ag --noheading --nobreak --nocolor --line-numbers $KEYWORD_DEF . > .easyopen_index
ag --noheading --nobreak --nocolor --line-numbers $KEYWORD_DEF  `bundle list --paths` >> .easyopen_index
