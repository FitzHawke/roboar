#!/usr/bin/env python
import math

def user_input_yn(question):
  user_input = input(question).lower()
  if user_input in ["q","quit"]:
    exit()
  elif user_input in ["n","no"]:
    return False
  else:
    return True

def user_input_list(candidates, question, queue = [], page_size = 10):
  count = 0
  for i in range(count, math.ceil(len(candidates) / page_size)):
    dict = {}
    for j in range(0,min(page_size, len(candidates) - i*page_size)):
      dict[j] = candidates[i*page_size+j]
      print(dict[j].number, " -- ", dict[j].name)
    
    user_input = input(question).split(",")
    if (user_input[0].lower() in ["q","quit"]):
      exit()
    elif len(user_input) == 1 and user_input[0] == "0":
      for key in dict.keys():
        queue.append(dict[key])
    else:
      for number in user_input:
        queue.append(dict[int(number)])

  return queue
