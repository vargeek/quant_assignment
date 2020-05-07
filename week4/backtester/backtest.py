import queue
from const import BAR, SIGNAL, ORDER, FILL
from handler import Handler
from event import Event
import logging
from datahandler import MDEngine
from strategy import Strategy
from portfolio import Portfolio
from execution import Execution

class BackTest():
    def __init__(self, config, create_handlers, register_handlers=None):

        self.event_queue = queue.Queue()

        self.data_handler, self.strategy, self.portfolio, self.execution = create_handlers(config, self.event_queue)

        assert isinstance(self.data_handler, MDEngine), type(self.data_handler)
        assert isinstance(self.strategy, Strategy), type(self.strategy)
        assert isinstance(self.portfolio, Portfolio), type(self.portfolio)
        assert isinstance(self.execution, Execution), type(self.execution)

        self._handlers = {}
        if register_handlers is None:
            self._register_handlers()
        else:
            register_handlers(self)

    def register_handler(self, event_type, handler):
        assert(event_type is not None)
        assert isinstance(handler, Handler), type(handler)

        handlers = self._handlers.get(event_type, None)
        if handlers is None:
            handlers = []
            self._handlers[event_type] = handlers
        handlers.append(handler)
        
    def _register_handlers(self):
        # BAR
        # update current bar; stop loss and profit target
        self.register_handler(BAR, self.portfolio)
        # cross orders in order_queue
        self.register_handler(BAR, self.execution)
        self.register_handler(BAR, self.strategy)
        
        # SIGNAL
        self.register_handler(SIGNAL, self.portfolio)

        # ORDER
        self.register_handler(ORDER, self.execution)

        # FILL
        self.register_handler(FILL, self.portfolio)

    def run_backtest(self):
        while True:
            # produce bar event
            should_continue = self.data_handler.publish_md()
            if not should_continue:
                self.execution.cancel_all_orders()
                self.portfolio.force_close_open_trades()
                break

            while True:
                # consume event_queue
                try:
                    event = self.event_queue.get(block=False)
                except queue.Empty:
                    break
                else:
                    if not isinstance(event, Event):
                        logging.error(f"invalid event type: {type(event)}")
                        raise Exception(f"invalid event type: {event}")

                    handlers = self._handlers.get(event.type, None)
                    if not isinstance(handlers, list) or len(handlers) == 0:
                        logging.error(f"unknown event type: {event}")
                        raise Exception(f"unknown event type: {event}")

                    for handler in handlers:
                        handler.handle_event(event)
