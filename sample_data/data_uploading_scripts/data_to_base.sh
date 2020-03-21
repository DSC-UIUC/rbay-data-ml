#!/bin/bash
input="data/names.txt" #this should be the path to the file of names
while IFS= read -r line
do
  python3 data_to_base.py $line 
  sleep 5
done < "$input"
