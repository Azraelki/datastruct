from nlp.commom.tool import load_dictionary, count_single_char, evaluate_speed


def fully_segment(text, dic):
    """
    全切分
    :param text: 文本
    :param dic: 字典
    :return: [(word, start, end)]
    """
    word_list = []
    for i in range(len(text)):                  # i 从 0 到text的最后一个字的下标遍历
        for j in range(i + 1, len(text) + 1):   # j 遍历[i + 1, len(text)]区间
            word = text[i:j]                    # 取出连续区间[i, j]对应的字符串
            if word in dic:                     # 如果在词典中，则认为是一个词
                word_list.append((word, i, j-1))
    return word_list


def forward_segment(text, dic):
    """
    最大正向匹配
    :param text: 文本
    :param dic: 字典
    :return:[(word, start, end)]
    """
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]                      # 当前扫描位置的单字
        end = i
        for j in range(i + 1, len(text) + 1):       # 所有可能的结尾
            word = text[i:j]                        # 从当前位置到结尾的连续字符串
            if word in dic:                         # 在词典中
                if len(word) > len(longest_word):   # 并且更长
                    longest_word = word             # 则更优先输出
                    end = i + len(word) - 1
        word_list.append((longest_word, i, end))    # 输出最长词
        i += len(longest_word)                      # 正向扫描
    return word_list


def backward_segment(text, dic):
    """
    最大逆向匹配
    :param text: 目标文本
    :param dic: 字典
    :return:[(word, start, end)]
    """
    word_list = []
    i = len(text) - 1
    while i >= 0:                                      # 扫描位置作为终点
        longest_word = text[i]                         # 扫描位置的单字
        start = i
        for j in range(0, i):                          # 遍历[0, i]区间作为待查询词语的起点
            word = text[j: i + 1]                      # 取出[j, i]区间作为待查询单词
            if word in dic:
                if len(word) > len(longest_word):      # 越长优先级越高
                    longest_word = word
                    start = j
                    break
        word_list.insert(0, (longest_word, start, i))  # 逆向扫描，所以越先查出的单词在位置上越靠后
        i -= len(longest_word)
    return word_list


def bidirectional_segment(text, dic):
    """
    双向匹配
    :param text: 目标文本
    :param dic: 字典
    :return: [(word, start, end)]
    """
    f = forward_segment(text, dic)
    b = backward_segment(text, dic)
    if len(f) < len(b):                                  # 词数更少优先级更高
        return f
    elif len(f) > len(b):
        return b
    else:
        if count_single_char(f) < count_single_char(b):  # 单字更少优先级更高
            return f
        else:
            return b


if __name__ == '__main__':
    mini_dic = load_dictionary()
    # 分词示例
    print('----' * 50)
    print('分词示例')
    print(' 全切分：', fully_segment('就读北京大学,研究生命起源', mini_dic))
    print('最大正向：', forward_segment('就读北京大学,研究生命起源', mini_dic))
    print('最大逆向：', backward_segment('就读北京大学,研究生命起源', mini_dic))
    print('双向匹配：', bidirectional_segment('就读北京大学,研究生命起源', mini_dic))

    # 分词速度评测
    text = '江西鄱阳湖干枯，中国最大淡水湖变成大草原,江西鄱阳湖干枯'
    print('----' * 50)
    print('分词速度评估')
    evaluate_speed(fully_segment, text, mini_dic)
    evaluate_speed(forward_segment, text, mini_dic)
    evaluate_speed(backward_segment, text, mini_dic)
    evaluate_speed(bidirectional_segment, text, mini_dic)
