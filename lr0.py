# coding=utf-8
__author__ = 'smallfly'

import reader
import lr0_analyser
import os

def parse(input_file, output_file, text):
    """
    根据LR(0)文法创建输出表
    :param input_file: 存储文法
    :param output_file: 输出的分析表
    :param text: 输入串
    :return:
    """
    # 读取出非终结符, 终结符, 产生式
    vn, vt, rules = reader.read_input(input_file, "~")
    print('rules:')
    # 输出rules
    for rule in rules:
        print("→".join(rule))
    print()
    action, goto = reader.read_output(output_file, vn, vt, "~")
    # 显示解析过程
    lr0_analyser.analyse(rules, action, goto, text)

def main():
    # input_file 是存储了文法的文件, 默认使用input1.txt这个文件
    input_file = input("input grammar file(input1.txt by default): ")
    if input_file.strip() == '':
        print("empty input, use default file")
        input_file = "input1.txt"

    # 检查文件是否存在
    if not os.path.exists(input_file):
        print("File:", input_file, "doesn't exist")
        return

    # 储存分析表的文件
    output_file = "table.txt"

    # 调用java程序
    command = "java -jar LRAnalyse.jar " + input_file + " " + output_file
    os.system(command)

    # 输入输入串
    print("input text(end by #): ")
    text = ""
    while True:
        text += input()
        if len(text) > 0 and text[-1] == '#':
            break

    print("text:", text)
    # 调用解析函数
    parse(input_file, output_file, text)


if __name__ == '__main__':
    main()
