# coding=utf-8
__author__ = 'smallfly'

"""
读取文件
"""

def read_input(filename, sep="~"):
    """
    从文件中读取非终结符, 终结符, 规则
    :param filename: 文件名
    :param sep: 分隔符
    :return: 非终结符, 终结符, 规则
    """
    rules = []
    with open(filename) as f:
        for i, line in enumerate(f, start=1):
            if i == 1:
                vn_str = line.strip()
            elif i == 2:
                vt_str = line.strip()
            else:
                rules.append(line.strip().split(sep))
    vn = vn_str.split(sep)
    vt = vt_str.split(sep)
    return vn, vt, rules

def read_output(filename, vn, vt, sep="~"):
    """
    从文件中读取出action, goto 表
    :param filename:
    :param vn: 非终结符
    :param vt: 终结符
    :return: action_table, goto_table
    """
    action = []
    goto = []
    with open(filename) as f:
        for line in f:
            chars = list(map(lambda x: x.strip(), line.strip().split(sep)))
            action_chars = chars[: len(chars) - len(vn)]
            todo_chars = chars[len(chars) - len(vn): -1]    # 每行以sep结尾
            action_row = dict()
            goto_row = dict()

            for i, char in enumerate(action_chars):
                if char != '@':
                    if i >= len(vt):
                        key = "#"
                    else:
                        key = vt[i]
                    action_row[key] = char
            action.append(action_row)

            for i, char in enumerate(todo_chars):
                if char != '@':
                    # i + 1 是为了跳过S
                    goto_row[vn[i + 1]] = int(char[1:])
            goto.append(goto_row)
        return action, goto


if __name__ == '__main__':
    pass

