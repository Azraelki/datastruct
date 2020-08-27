import os
import json


class LogManager:
    """
    日志管理器
    """

    def __init__(self, path: str):
        """
        path 文件目录
        :param path:目录路径
        """
        if not os.path.exists(path):
            os.mkdir(path)
        self.file_path = path + '/log.json'
        self.logs = []
        self.restore()

    def store(self):
        """
        持久化当前日志信息
        :return:
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=4)
            f.flush()
            f.close()

    def restore(self):
        """
        从本地恢复日志
        :return:
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.logs = json.load(f)
        else:
            self.logs = []

    @property
    def last_log_index(self):
        """
        最大索引号
        :return:
        """
        return len(self.logs) - 1

    @property
    def last_log_term(self):
        """
        最大任期号
        :return:
        """
        return self.get_term_by_index(self.last_log_index)

    def get_term_by_index(self, index):
        """
        根据索引查询日志任期号
        :param index: 索引号
        :return:
        """
        if index < 0 or index >= len(self.logs):
            return -1
        return self.logs[index]['term']

    def append_log(self, log: dict):
        """
        添加日志信息
        :param log: 日志记录
        :return:
        """
        self.logs.append(log)
        # 持久化
        self.store()

    def delete_logs(self, index):
        """
        删除指定索引及之后所有的日志记录
        :param index:
        :return:
        """
        self.logs = self.logs[0: max(0, index)]
        # 持久化
        self.store()

    def get_logs(self, begin_index, end_index=None):
        """
        获取指定索引之后的所有日志记录
        :param begin_index: 开始位置
        :param end_index:  结束位置，默认为末尾
        :return:
        """
        if end_index and end_index <= len(self.logs):
            return self.logs[max(0, begin_index): end_index]
        else:
            return self.logs[max(0, begin_index):]

    def get_log_by_index(self, index):
        """
        根据索引获取日志
        :param index:
        :return:
        """
        if len(self.logs) == 0 or index < 0 or index >= len(self.logs):
            return None
        return self.logs[index]
