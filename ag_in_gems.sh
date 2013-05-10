#!/bin/bash

ag --noheading --nobreak --nocolor --line-numbers $1  `bundle list --paths`
