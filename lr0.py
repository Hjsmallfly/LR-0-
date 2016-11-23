# coding=utf-8
__author__ = 'smallfly'

import reader
import lr0_parser

def main():
    vn, vt, rules = reader.read_input("input.txt")
    # print(vn, vt, rules)
    # print(rules)
    action, goto = reader.read_output("output.txt", vn, vt)
    # print(goto)
    lr0_parser.parse(rules, action, goto,"ad#")

if __name__ == '__main__':
    main()
