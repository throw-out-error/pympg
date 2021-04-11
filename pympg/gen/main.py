from abc import ABC, abstractmethod


class ConfigGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate():
        raise NotImplementedError()

    @abstractmethod
    def reload():
        raise NotImplementedError()
