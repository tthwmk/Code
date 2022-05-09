from abc import abstractmethod, ABCMeta


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def get_entries(self):
        """
        returns entries signals
        """
        pass

    @abstractmethod
    def get_exits(self):
        """
        returns exit signals
        """
        pass
