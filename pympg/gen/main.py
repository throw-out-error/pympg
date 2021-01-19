from abc import ABC, abstractclassmethod


class ConfigGenerator(ABC):
    @abstractclassmethod
    def generate():
        raise NotImplementedError()

    @abstractclassmethod
    def reload():
        raise NotImplementedError()
