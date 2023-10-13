#!/usr/bin/env bash

find source -name "*.md" \
    | while read file; do
        echo "processing: '$file'"
        cat "$file" \
            | sed -n -e '/^---/,/^---/p' \
            | sed -e '/^---/d' \
            | grep -e '^title:\|^date:' \
            > $(dirname "$file")/meta
      done  


