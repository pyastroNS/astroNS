# -*- coding: utf-8 -*-
from simpy.core import Environment
from typing import List, Dict, Tuple, Any, Optional, Callable

import numpy as np

from nodes.core.base import BaseNode
from links.predicates import patterns
from common.left_side_value import left_side_value


class Maximizer(BaseNode):
    def __init__(self, env: Environment, name: str, configuration: Dict[str, Any]):
        """Initialize the node"""
        super().__init__(env, name, configuration, self.execute())
        self._key: str = self.configuration.get("key", "KEY")
        # This is a list of text strings that contain the values to be compared
        self._time_delay: Callable[[], Optional[float]] = self.setFloatFromConfig(
            "time_delay", 0.00
        )

        self.env.process(self.run())

    @property
    def time_delay(self) -> Optional[float]:
        return self._time_delay()

    def execute(self):
        """The simpy execution loop"""
        delay: float = 0.0
        processing_time: float = delay
        data_out_list: List[Tuple] = []
        fields = []
        num_messages = 0
        while True:
            data_in = yield (delay, processing_time, data_out_list)

            if data_in:
                delay = self.time_delay
                processing_time = delay

                # print(data_in[self._key])
                try:
                    max_value = max(data_in[self._key])
                except:
                    print(
                        "{} This node had an error associated with the message:".format(
                            self.log_prefix(data_in["ID"])
                        )
                    )
                    print(data_in)
                    max_value = []

                print(
                    "{} Message with list of values received, minimum value was {}.".format(
                        self.log_prefix(data_in["ID"]), max_value
                    )
                )
                data_out = data_in.copy()
                data_out[self._key] = max_value
                data_out_list = [data_out]
            else:
                data_out_list = []
