#!/usr/bin/env python
import math


def user_input_yn(question):
    user_input = input(question).lower()
    if user_input in ["q", "quit"]:
        exit()
    elif user_input in ["n", "no"]:
        return False
    else:
        return True


def user_input_list(candidates, question, queue=[], page_size=10):
    for i in range(0, math.ceil(len(candidates) / page_size)):
        print(i)
        dict = {}
        for j in range(0, min(page_size, len(candidates) - i * page_size)):
            curr = candidates[i * page_size + j]
            dict[curr.number] = curr
            print(curr.number, " -- ", curr.name)

        user_input = input(question).split(",")
        if user_input[0].lower() in ["q", "quit"]:
            exit()
        elif len(user_input) == 1 and user_input[0] == "0":
            for key in dict.keys():
                queue.append(dict[key])
        elif user_input[0] == "":
            continue
        else:
            for number in user_input:
                queue.append(dict[int(number)])

    return queue
