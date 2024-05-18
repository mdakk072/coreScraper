"""
BaseFSM Module

This module provides a base class for implementing a finite state machine (FSM) for web scraping processes. 
It includes basic states and methods for running and transitioning between states. Specific FSM logic 
should be implemented in subclasses.

Classes:
    BaseState: An enumeration of basic states for the FSM.
    BaseFSM: A base class for creating FSMs with customizable states and logic.

Usage Example:
    from core.base_fsm import BaseFSM, BaseState

    class MyScraperState(BaseState):
        FETCH_DATA = auto()
        PARSE_DATA = auto()
        SAVE_DATA = auto()

    class MyScraperFSM(BaseFSM):
        def fsm(self):
            if self.current_state == BaseState.INITIAL:
                return MyScraperState.FETCH_DATA
            elif self.current_state == MyScraperState.FETCH_DATA:
                # Implement fetching logic here
                return MyScraperState.PARSE_DATA
            elif self.current_state == MyScraperState.PARSE_DATA:
                # Implement parsing logic here
                return MyScraperState.SAVE_DATA
            elif self.current_state == MyScraperState.SAVE_DATA:
                # Implement saving logic here
                return BaseState.END
            else:
                return BaseState.END

    fsm = MyScraperFSM()
    fsm.run()
"""

from core.utils import Utils
from enum import Enum, auto
from typing import Type

class BaseState(Enum):
    """
    BaseState defines the fundamental states for the FSM.
    Additional specific states should be added in child classes.

    Attributes:
        INITIAL: The initial state of the FSM.
        END: The end state of the FSM.
    """
    INITIAL = auto()
    END = auto()

class BaseFSM:
    """
    BaseFSM is a base class for implementing a finite state machine (FSM) for web scraping processes.

    The class provides methods for initializing the FSM, running the FSM loop, and transitioning
    between states. Specific FSM logic should be implemented in subclasses.

    Attributes:
        logger (logging.Logger): A logger for logging FSM activities.
        current_state (BaseState): The current state of the FSM.
    """

    def __init__(self, **kwargs):
        """
        Initialize the BaseFSM with configuration options.

        Args:
            **kwargs: Arbitrary keyword arguments representing configuration options.
        """
        self.logger = Utils.get_logger()
        self.current_state = BaseState.INITIAL

        # Load configuration from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        # Additional initialization if needed
        self._initialize()

    def _initialize(self):
        """
        Additional initialization steps can be implemented by subclasses.
        """
        pass

    def run(self):
        """
        Run the FSM, transitioning through states until reaching the END state.

        This method logs the start and end of the FSM run and handles exceptions that occur
        during state transitions.
        """
        self.logger.info("Starting FSM run.")
        while self.current_state != BaseState.END:
            self.logger.debug("Current state: %s", self.current_state.name)
            try:
                self.current_state = self.fsm()
            except Exception as e:
                self.logger.error(f"Error in state {self.current_state.name}: {e}")
                break
        self.logger.info("FSM run completed.")

    def fsm(self) -> Type[BaseState]:
        """
        Define the FSM logic.

        This method should be implemented by subclasses to specify the logic for transitioning
        between states based on the current state and actions performed.

        Returns:
            BaseState: The next state of the FSM.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def transition_to(self, new_state: Type[BaseState]):
        """
        Utility method for transitioning to a new state.

        Args:
            new_state (BaseState): The new state to transition to.
        """
        self.logger.info(f"Transitioning from {self.current_state.name} to {new_state.name}")
        self.current_state = new_state
