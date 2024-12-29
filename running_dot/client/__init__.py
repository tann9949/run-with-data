from abc import ABC, abstractmethod


class BaseClient(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.setup()

    @abstractmethod
    def setup(self):
        raise NotImplementedError()