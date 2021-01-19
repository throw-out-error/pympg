from abc import ABC, abstractmethod


class ConfigGenerator(ABC):
    @abstractmethod
    def generate():
        raise NotImplementedError()

    @abstractmethod
    def reload():
        raise NotImplementedError()
