# coding=utf-8
__author__ = 'smallfly'

"""
输出结果
"""

# 常量
ACCEPT = "A"

# 测试用例
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
        dict(),
        {"A": 3},
        dict(),
        dict(),
        {"B": 7},
        dict(),
        dict(),
        dict(),
        dict(),
    ]

    return [action, goto]

def parse_action(action):
    """

    :param action: 形如 s1 r2 A(接受) 之类的字符串
    :return: (类型, 数字)
    """
    type_ = action[0]
    try:
        num = int(action[1: ])
    except ValueError as e:
        num = 0
    return (type_, num)

def get_action(action_table, status_stack, input_string):
    """
    获取下一个动作
    :param action_table: 动作矩阵
    :param status_stack: 状态栈
    :param input_string: 输入串
    :return: 动作 | None
    """
    # 获取状态栈顶部的状态
    status_top = status_stack[-1]
    # 输入串的第一个字符
    char = input_string[0]
    # 获取该状态行
    row = action_table[status_top]
    # 如果遇到该输入字符没有定义动作, 那么说明是错误的输入, 返回None
    if char not in row:
        return None
    action = row[char]
    return action

def get_goto(goto_table, status_stack, left):
    row = goto_table[status_stack[-1]]
    if left not in row:
        return None
    return row[left]

def parse(L, input_str):
    """
    判断input_str是否符合文法L
    :param L: 文法, 产生式 [(左部, 右部), ...]
    :param input_str: 输入串
    :return:
    """
    text = "%-23s %-20s %-20s %-27s %-20s" % ("状态", "符号栈", "输入字符串", "action", "goto")
    print(text)

    # 记录步数
    step = 0
    # 根据文法获取LR(0)分析表
    action_table, goto_table = get_table(L)
    # 状态栈
    status_stack = [0]
    # 符号栈
    symbol_stack = ["#"]

    # goto项
    goto = None

    while True:

        step += 1

        # 获取动作
        action = get_action(action_table, status_stack, input_str)

        if action is None:
            print("出错")
            return
        # 解析该动作
        action_type, num = parse_action(action)

        # 在此处补充一下goto
        if action_type == 'r':
            left_part, right_part = L[num - 1]  # 下标从0开始
            tmp_stack = [ status_stack[len(status_stack) - len(right_part) - 1] ]
            goto = get_goto(goto_table, tmp_stack, left_part)
        else:
            goto = ""

        text = "%-25s %-25s %-25s %-25s %-25s" % (status_stack, "".join(symbol_stack), input_str, action, goto)
        print(text)

        # 这下面开始为下一个步骤表格填充数据

        # 移进
        if action_type == "s":
            # 只有r的情况有goto
            goto = None
            # 状态栈加入这个状态
            status_stack.append(num)
            # 符号栈加入第一个符号
            symbol_stack.append(input_str[0])
            # 输入串截断
            if len(input_str) > 1:
                input_str = input_str[1:]
        # 接受
        elif action_type == ACCEPT:
            goto = None
            print("Parse finished: Accepted!")
            return
        # 规约
        elif action_type == "r":
            # 规约使用的产生式
            left_part, right_part = L[num - 1]  # 下标从0开始
            # 此处规约消耗的字符数
            len_right_part = len(right_part)
            # 去掉符号栈的相应字符, 用规约结果代替
            for i in range(len_right_part):
                symbol_stack.pop()
            symbol_stack.append(left_part)

            # 同时去掉状态栈相应个数个状态
            for i in range(len_right_part):
                status_stack.pop()

            # 获取goto表中的内容
            goto = get_goto(goto_table, status_stack, left_part)
            if goto is None:
                print("出错")
                return
            # row = goto_table[status_stack[-1]]
            # if left_part not in row:
            #     print("ERROR@Char:", left_part)
            #     return
            # goto = row[left_part]
            status_stack.append(goto)



if __name__ == '__main__':
    parse(PRODUCE_EXPRESSIONS, "abbcde#")

