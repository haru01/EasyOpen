#!/bin/bash
rm .easyopen_index

exp='(def\s|class\s|modlue\s|\sattr_accessor\s|\sattr_reader\s|\sattr_accessor\s|\sscope\s|\sclass_attribute\s|\sbelongs_to\s|\shas_many\s|\sattr_readonly\s)'
ag --noheading --nobreak --nocolor --line-numbers $exp . > .easyopen_index
ag --noheading --nobreak --nocolor --line-numbers $exp  `bundle list --paths` >> .easyopen_index
