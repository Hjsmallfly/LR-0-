# coding=utf-8
__author__ = 'rmallfly'

"""
输出结果
"""

ACCEPT = "A"

PRODUCE_EXPRESSIONS = [
    ("S", "aAcBe"),
    ("A", "b"),
    ("A", "Ab"),
    ("B", "d")
]

def get_table(L):
    """
    根据输入的文法构造出LR(0)分析表
    :param L: 文法
    :return:
    """
    # 二维数组
    action = [
        #0
        {"a": "s2"},
        {"#": ACCEPT},
        {"b": "s4"},
        {"c": "s5", "b": "s6"},
        {"a": "r2", "c": "r2", "e": "r2", "b": "r2", "d": "r2", "#": "r2"},
        {"d": "s8"},
        {"a": "r3", "c": "r3", "e": "r3", "b": "r3", "d": "r3", "#": "r3"},
        {"e": "s9"},
        {"a": "r4", "c": "r4", "e": "r4", "b": "r4", "d": "r4", "#": "r4"},
        {"a": "r1", "c": "r1", "e": "r1", "b": "r1", "d": "r1", "#": "r1"},
    ]

    goto = [
        #0
        {"S": 1},
        {},
        {"A": 3},
        {},
        {},
        {"B": 7},
        {},
        {},
        {},
        {},
    ]

    return [action, goto]

def parse_action(action):
    type_ = action[0]
    # print("->", action[1:])
    try:
        num = int(action[1: ])
    except ValueError as e:
        num = 0
    return (type_, num)

def get_next_action(action_table, status_stack, input_string):
    status_top = status_stack[-1]
    # print("Status Top is:", status_top)
    # 输入串的第一个字符
    char = input_string[0]
    # print("Char is:", char)
    # 和该状态有关的行
    row = action_table[status_top]
    if char not in row:
        return None
    # try:
    action = row[char]
    # except TypeError as e:
    #     print(row)
    #     print(type(row))
    #     input()
    return action

def parse(L, input_str):

    action_table, goto_table = get_table(L)
    # 状态栈
    status_stack = [0]
    # 符号栈
    symbol_stack = ["#"]
    # 动作
    action = None
    # GOTO
    goto = None

    step = 1

    break_condition = False

    action = get_next_action(action_table, status_stack, input_str)
    # print(status_stack, symbol_stack, input_str, action, goto)
    print(status_stack, "".join(symbol_stack), input_str)

    if action is None:
        print("出错")
        return
    first_time = True

    while not break_condition:
        # 获取动作
        # action = get_next_action(action_table, status_stack, input_str)
        # if action is None:
        #     print("出错")
        #     return

        if first_time:
            # print(status_stack, symbol_stack, input_str, action, goto)
            first_time = False
        else:
            action = get_next_action(action_table, status_stack, input_str)

        if action is None:
            print("出错")
            return
        action_type, num = parse_action(action)

        if action_type == "s":
            # 状态栈加入这个状态
            status_stack.append(num)
            # 符号栈加入第一个符号
            symbol_stack.append(input_str[0])
            # 输入串截断
            if len(input_str) > 1:
                input_str = input_str[1:]

        elif action_type == ACCEPT:
            print("Parse finished: Accepted!")
            break_condition = True
            return
        elif action_type == "r":
            # input("r step")
            step += 1
            # 规约动作
            # 规约使用的产生式
            left_part, right_part = L[num - 1]
            len_right_part = len(right_part)
            # 去掉符号栈的相应字符, 用规约结果代替
            # input_str = input_str[len_right_part:]
            # print("---------->", input_str)
            # input_str += left_part
            # symbol_stack
            for i in range(len_right_part):
                symbol_stack.pop()
            symbol_stack.append(left_part)
            # print("--------->", symbol_stack)
            # 状态栈同时去掉相应个数个状态
            for i in range(len_right_part):
                status_stack.pop()
            row = goto_table[status_stack[-1]]
            # print("-------->", row)
            # print(L[num])
            if left_part not in row:
                print("ERROR@Char:", left_part)
                return
            goto = row[left_part]
            status_stack.append(goto)
        # else:
        #     print(action_type)
        #     input()

        # print(status_stack, symbol_stack, input_str, action, goto)
        print(status_stack, "".join(symbol_stack), input_str)
        # print(status_stack, symbol_stack, input_str)


if __name__ == '__main__':
    parse(PRODUCE_EXPRESSIONS, "abbcde#")

