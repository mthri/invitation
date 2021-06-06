from abc import ABC, abstractproperty, abstractmethod


class BaseMessenger(ABC):

    @abstractproperty
    def name(self) -> str:
        ...

    @abstractproperty
    def short_name(self) -> str:
        '''
        return 3 character
        '''
        ...

    @abstractproperty
    def description(self) -> str:
        ...

    @abstractproperty
    def is_primary(self) -> bool:
        ...

    @abstractproperty
    def has_cost(self) -> bool:
        ...

    @abstractproperty
    def price_per_message(self) -> int:
        ...

    @abstractmethod
    def send(self, contact, message: str) -> bool:
        ...

    @abstractmethod
    def save_contact(contacts) -> bool:
        ...


class TelegramMessenger(BaseMessenger):

    NAME = 'Telegram'
    SHORT_NAME = 'TLG'

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def short_name(self) -> str:
        return self.SHORT_NAME

    @property
    def description(self) -> str:
        return 'Telegram Messenger'

    @property
    def has_cost(self) -> bool:
        return False

    @property
    def is_primary(self) -> bool:
        return False

    @property
    def price_per_message(self) -> int:
        return 0

    def send(self, contact, message: str) -> bool:
        raise NotImplementedError

    def save_contact(contacts) -> bool:
        raise NotImplementedError
