from typing import Type
import pytest
from core.baseFSM import BaseFSM, BaseState
from enum import Enum, auto

class MockState(Enum):
    INITIAL = auto()
    STATE1 = auto()
    STATE2 = auto()
    STATE3 = auto()
    END = auto()

class MockFSM(BaseFSM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execution_order = []

    def fsm(self) -> Type[BaseState]:
        if self.current_state == BaseState.INITIAL:
            self.execution_order.append('INITIAL')
            return MockState.STATE1
        elif self.current_state == MockState.STATE1:
            self.execution_order.append('STATE1')
            return MockState.STATE2
        elif self.current_state == MockState.STATE2:
            self.execution_order.append('STATE2')
            return MockState.STATE3
        elif self.current_state == MockState.STATE3:
            self.execution_order.append('STATE3')
            return BaseState.END
        else:
            return BaseState.END

@pytest.fixture
def fsm():
    return MockFSM()

def test_initial_state(fsm):
    assert fsm.current_state == BaseState.INITIAL

def test_transition_to(fsm):
    fsm.transition_to(MockState.STATE1)
    assert fsm.current_state == MockState.STATE1

def test_run_fsm(fsm):
    fsm.run()
    assert fsm.current_state == BaseState.END
    assert fsm.execution_order == ['INITIAL', 'STATE1', 'STATE2', 'STATE3']

def test_exception_handling(mocker):
    class ExceptionFSM(BaseFSM):
        def fsm(self):
            raise ValueError("Test Exception")

    mock_logger = mocker.patch('core.utils.Utils.get_logger')

    fsm = ExceptionFSM()
    fsm.run()
    assert fsm.current_state == BaseState.INITIAL
    mock_logger().error.assert_called_with("Error in state INITIAL: Test Exception")
