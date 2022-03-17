# -*- coding: utf-8 -*-
"""DelayTime is a node that delays a message for a set amount of time."""
from simpy.core import Environment
from typing import List, Dict, Tuple, Any, Optional, Callable

from nodes.core.base import BaseNode


class KeyDelayTime(BaseNode):
    """Node for implementing a static time delay

    This class contains the node useful for implementing a static delay, but does
    not have any methods for implementing a delay based on other variables like
    a processing rate.

    """

    def __init__(self, env: Environment, name: str, configuration: Dict[str, Any]):
        """Initialize the node"""
        super().__init__(env, name, configuration, self.execute())
        self._time_delay_key: Callable[[], Optional[float]] = self.setStringFromConfig(
            "delay_key", "key"
        )
        self.env.process(self.run())

    # @coroutineSend
    def execute(self):
        """Execute function for the delay node"""
        delay: float = 0.0
        processing_time: float = 0.0
        data_in: Tuple[float, float, List[Tuple]] = None
        data_out_list: List[Tuple] = []
        while True:
            # Prime the node and wait for the yield to return a message.
            data_in = yield (delay, processing_time, data_out_list)
            # A message has arrived
            if data_in:
                # The delay is what is set by the node
                try:
                    delay = data_in[self._time_delay_key()] - self.env.now
                except:
                    print(data_in)
                    delay = 0
                # Add the time to the total processing on this node
                processing_time = delay
                # Make a copy of the data at this time
                data_out_list = [data_in.copy()]
                # Print to log
                print(
                    self.log_prefix(data_in["ID"])
                    + "Data ID |%s| arrived at |%f|. Delay set to |%f| simtime units"
                    % (data_in["ID"], self.env.now, delay)
                )
            else:
                # No message has arrived, don't send any messages out.
                data_out_list = []
