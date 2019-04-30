# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Wenyuan Wu, 18746867
# Author: Gian-Luca Kuoni - 17739822
# Date: 28.04.2019
# Additional Info:

import gzip
import random
import xml.etree.ElementTree as ET
from typing import BinaryIO
from pathlib import Path


def split_corpus(infile: BinaryIO, targetdir: str, n: int=1000):
    """
    This function takes as arguments the corpus opened for reading in binary mode, the output directory,
    and the size of the test and dev set. The function has no return value,
    but should generate three compressed files in the specified output directory:
    abstracts.txt.training.gz
    abstracts.txt.test.gz
    abstracts.txt.development.gz
    :param infile: a binary file-like object
    :param targetdir: a string which indicates the output directory
    :param n: the size of the test and dev set
    :return: None
    """
    data_folder = Path(targetdir)
    train_path = data_folder / 'abstracts.txt.training.gz'
    test_path = data_folder / 'abstracts.txt.test.gz'
    dev_path = data_folder / 'abstracts.txt.development.gz'

    # generate a list which contains randomly selected samples and write other unselected items into training set
    train_output = gzip.open(str(train_path), mode='wb')
    reservoir = []
    res_num = 2 * n
    sents_enum = enumerate(item[1].text for item in ET.iterparse(infile) if item[1].tag == 'sentence')
    for t, item in sents_enum:
        if t < res_num:
            reservoir.append(item)
        else:
            m = random.randint(0, t)
            if m < res_num:
                train_output.write(reservoir[m].encode('utf-8'))
                reservoir[m] = item
            else:
                train_output.write(item.encode('utf-8'))
        print('{} sentences processed'.format(t))
    train_output.close()

    # spilt all samples into two equal parts, first half will treat as test set and second will be dev set
    test_output = gzip.open(str(test_path), mode='wb')
    dev_output = gzip.open(str(dev_path), mode='wb')
    counter = 0
    for item in reservoir:
        if counter < n:
            test_output.write(item.encode('utf-8'))
            test_output.write(b'\n')
            counter += 1
        elif counter >= n:
            dev_output.write(item.encode('utf-8'))
            dev_output.write(b'\n')
            counter += 1
    test_output.close()
    dev_output.close()


def main():
    data_folder = Path('Korpusdaten/')
    file_to_open = data_folder / "abstracts.xml.gz"
    roh_data = gzip.open(str(file_to_open), 'rb')
    split_corpus(roh_data, 'Korpusdaten/')


if __name__ == '__main__':
    main()
