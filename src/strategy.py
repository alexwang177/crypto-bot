from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def take_action(self):
        pass
