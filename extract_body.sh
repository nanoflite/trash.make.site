#!/usr/bin/env bash

find source -name "*.md" \
    | while read file; do
        echo "processing: '$file'"
        cat "$file" \
            | sed -e '/^---/,/^---/d' \
            | sed -e '1{/^$/d}' \
            > $(dirname "$file")/body.md
      done  


