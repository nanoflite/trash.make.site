#!/usr/bin/env bash

# | sed -e ':a;N;$!ba;s/\n/ /g' \

find source -name "meta" \
    | while read file; do
        echo "processing: '$file'"
        cat "$file" \
            | sed -e 's/:\s*/=/' -e 's/[a-z]*[A-Z]*=/\U&/g' \
            > $(dirname "$file")/env
      done  


