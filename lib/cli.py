# encoding=utf-8

import argparse
import os
import platform
import sys


class ScriptExecutor:
    """
        脚本化Script， 主要是使用argparse
    """
    def __init__(self, commend, args):
        self.commend = commend.lower()
        self.args = args


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a argparse sample')
    sub_parsers = parser.add_subparsers(title='Please Choose a item')
    extract_sub_parser = sub_parsers.add_parser('extract', help="extract item")
    extract_sub_parser.add_argument('file', help="input file path")
    train_sub_parser = sub_parsers.add_parser('train', help="train item")
    convert_sub_parser = sub_parsers.add_parser('convert', help="convert item")
    print parser.parse_args()



