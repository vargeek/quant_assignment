from abc import ABC

class Handler(ABC):
    def handle_event(self, event):
        name = f"handle_{event.type.lower()}"
        fn = getattr(self, name, None)
        if fn is None:
            raise NotImplementedError(f"Should implement {self.__class__} {name}!")
        fn(event)
