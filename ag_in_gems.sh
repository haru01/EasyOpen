#!/bin/bash

# NOTE:  python Popen から うまく行番号が出なかったので代替案で、--ackmate オプションをつけて sed でフォーマットし直し
ag --noheading --nobreak --nocolor --ackmate $1  `bundle list --paths` | sed 's/^://' | sed 's/;[0-9 ]*://'
