#!/bin/bash
rm .easyopen_index

exp='(def\s|class\s|modlue\s)'
ag --noheading --nobreak --nocolor --line-numbers $exp . > .easyopen_index
ag --noheading --nobreak --nocolor --line-numbers $exp  `bundle list --paths` >> .easyopen_index
