# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Wenyuan Wu, 18746867
# Author: Gian-Luca Kuoni - 17739822
# Date: 28.04.2019
# Additional Info:

import gzip
import json
import bz2
from typing import BinaryIO
from pathlib import Path


def mk_meme_corpus(infile: BinaryIO,
                   outfile: str,
                   min_score: int=100,
                   min_len: int=1,
                   max_len: int=50):
    """
    This function is to extract reddit comments which satisfy specified filter parameters and write all these comments
    into a gzip compressed file in binary mode.
    :param infile: a binary file-like object
    :param outfile: the name of the output corpus
    :param min_score: the minimal number of upvotes(likes), default 100
    :param min_len: the minimal length of comments, default 1
    :param max_len: the maximal length of comments, default 50
    :return: None
    """
    data_folder = Path('Korpusdaten/')
    file_to_write = data_folder / outfile
    output_file = gzip.open(str(file_to_write), mode='wb')
    sents_hashes = set()
    counter = 0
    for sents in infile:
        # convert json format into python dictionary
        sents_dic = json.loads(sents.decode('utf-8'))
        sents_len = len(sents_dic['body'])
        sents_hash = hash(sents_dic['body'])

        if sents_dic['score'] >= min_score \
                and sents_len in range(min_len, (max_len + 1)) \
                and sents_hash not in sents_hashes:
            sents_hashes.add(sents_hash)
            output_file.write(sents_dic['body'].encode('utf-8'))
            counter += 1
            print('{} sentences processed'.format(counter))
    output_file.close()


def main():
    data_folder = Path('Korpusdaten/')
    file_to_open = data_folder / "RC_2012-06.bz2"
    roh_data = bz2.open(str(file_to_open), mode='rb')
    mk_meme_corpus(roh_data, 'RC_deduplication.txt.gz')


if __name__ == '__main__':
    main()
