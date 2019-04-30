# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Wenyuan Wu, 18746867
# Author: Gian-Luca Kuoni - 17739822
# Date: 28.04.2019
# Additional Info:

from typing import Iterable


def longest_substrings(x: str, y: str) -> Iterable[str]:
    """
    This function takes as arguments two different strings and returns the longest substring(s) in an iterable.
    :param x: first string
    :param y: second string
    :return: a list of longest substring(s) or None if there is no match
    """
    result = []
    x = x.lower()
    y = y.lower()
    len_x = len(x)
    len_y = len(y)
    for pos_x in range(len_x):
        for pos_y in range(len_y):
            temp = ""
            counter = 0
            while((pos_x + counter < len_x)
                  and (pos_y + counter < len_y)
                  and x[pos_x + counter] == y[pos_y + counter]):
                temp += y[pos_y + counter]
                result.append(temp)
                counter += 1
    if len(result) > 0:
        max_length = max(len(item) for item in result)
        return [item for item in result if len(item) == max_length]
    else:
        return None


def main():
    print(longest_substrings('Tod', 'Leben'))
    print(longest_substrings('Haus', 'Maus'))
    print(longest_substrings('mozart', 'mozzarella'))
    print(longest_substrings('keep the interface!', 'KeEp ThE iNtErFaCe!'))


if __name__ == '__main__':
    main()
