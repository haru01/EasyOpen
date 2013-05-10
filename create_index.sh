#!/bin/bash

rm .easyopen_index
exp='(def\s|class\s|modlue\s)'
ag --noheading --nobreak --nocolor --ackmate $exp  `bundle list --paths` | sed 's/^://' | sed 's/;[0-9 ]*://' > .easyopen_index
ag --noheading --nobreak --nocolor --ackmate $exp | sed 's/^://' | sed 's/;[0-9 ]*://' >> .easyopen_index
