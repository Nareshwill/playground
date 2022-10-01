#!/bin/sh

str='foo\nbar\nbaz'

while [[ $str ]]; do            # iterate as long as we have input
  if [[ $str = *'\n'* ]]; then  # if there's a '\n' sequence later...
    first=${str%%'\n'*}         #   put everything before it into 'first'
    rest=${str#*'\n'}           #   and put everything after it in 'rest'
  else                          # if there's no '\n' later...
    first=$str                  #   then put the whole rest of the string in 'first'
    rest=''                     #   and there is no 'rest'
  fi
  echo "Processing piece: $first"
  str=$rest
done