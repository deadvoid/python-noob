#!/usr/bin/env python 
### for best practice use env python instead of direct path. remove >this< comment ##
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

  Define the extract_names() function below and change main()
  to call it.

  For writing regex, it's nice to include a copy of the target
  text for inspiration.

  Here's what the html looks like in the baby.html files:
  ...
    <h3 align="center">Popularity in 1990</h3>
    ....
    <tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
    <tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
    <tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
  ...

  Suggested milestones for incremental development:
   1. Extract the year and print it
   2. Extract the names and rank numbers and just print them
   3. Get the names data into a dict and print it
   4. Build the [year, 'name rank', ... ] list and print it
   5. Fix main() to use the extract_names list
"""

def extract_names(filename):
  # extract_names() uses input filename as argument
  # create a list called names
  babynames = []

  # Open and read the file.
  f = open(filename, 'rU')
  text = f.read()

  # Milestone #1.
    # Could process the file line-by-line, but regex on the whole text
    # at once is even easier.
    # Get the year. Use search()
  year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)

  # If we didn't find a year, we'll exit with an error message.
  if not year_match:
    sys.stderr.write("Couldn't find the year searched!\n")
    sys.exit(1)

  # use variable year as container to re search result
  year = year_match.group(1)  
  ###
    # print "year_match is: ", type(year_match) # result <type '_sre.SRE_Match'>
    # print "year is:", year, "type:", type(year) # result <type 'str'>
  
  # append the result to list 'names'
  babynames.append(year)

  # Milestone #2. 
  # Get the ranks & name, use findall()
  name_rank_match = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', text)
  ### re search result
    # print the search result
    # print "name_rank_match : ", name_rank_match
    # So name_rank_match is a list with tuple in each entry.
  
  # Milestone #3. 
    # Get the names data into a dict and print it
    # Create a dict & fill it with the name_rank_match list tuples
  babynames_scrap = {}

  ### Dict notes
    # print dict.update will always return None
    # keys are unique in dict, so using rank number as key will overwrite existing values
    # a single rank number is assigned to both male & female 
    # hence, names are used as key and rank number is used for values instead
  for (rank, male, female) in name_rank_match:
    ### notes on key:values entry
      # babynames_scrap.update({male:rank, female:rank})
      # this works, but the same name that appears for male & female in diff rank
      # means the later will overwrite existing key:value entry. avoid.
      # let's try adding using rank as key, and pair to values of male,female tuple
    babynames_scrap.update({int(rank):(male,female)})
    # that works nicer so let's use this instead

  # print "Dict babynames_scrap : ", babynames_scrap
  
  # Milestone #4. 
    # Build the [year, 'name rank', ... ] list and print it
    # ok so the way i see it, let's make it look like this table
    # >> 1990
    # >> 1. Boy : <male name>, Girl : <female name>
    # >> 2. Boy : <male name>, Girl : <female name>
    # etc. 
    # First let's sort the <keys:values> pair and insert it to 'babynames' list
    # Make sure what kind of type rank number in babynames_scrap dict first
    # print babynames_scrap.has_key(1) # <- false; meaning the keys are * strings *
		# update rank in line 91 : babynames_scrap.update() to int(rank)
  sort_by_rank = sorted(babynames_scrap.keys())

  for rank in sort_by_rank:
    sorted_entry = rank, babynames_scrap[rank]
    babynames.append(sorted_entry)
		
  return babynames


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # Milestone #4. For each filename, get the names, then either print 
  # the text output or write it to a summary file

  ### printed text output
  for filename in args:
    # print filename
    ranked_names = extract_names(filename)
    # Get list length
    length = len(ranked_names)
    # Print the Headline - year first
    print "-"*40, "\nPopular Names by Birth Year", ranked_names[0], "\n", "Rank\tBoy\t\t\tGirl\n", "-"*40
    # Print the scraped data : rank, male & female name
    for i in range(1, length):
      print ranked_names[i][0], "\t", ranked_names[i][1][0], "\t\t", ranked_names[i][1][1]

  ### yet for summary file dump
	#	TODO 

# boilerplate : if name called is self, then run it; else do nothing
if __name__ == '__main__':
  main()
