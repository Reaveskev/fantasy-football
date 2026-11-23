import pytest
from backtest_data import mae, bias



# Run test .venv/Scripts/python.exe -m pytest

def test_mae_empty_raises():
    # An empty list should raise, not return 0. A 0 would look like
    # perfect projections and hide an upstream bug 
    with pytest.raises(ValueError):
        mae([])
        

    

def test_bias_empty_raises():
    # An empty list should raise, not return 0. A 0 would look like
    # no lean either way 
    with pytest.raises(ValueError):
        bias([])



def test_high_bias():
    # Projections that run too high should give a positive bias.
    # Locks in the sign convention: positive = projected too high.
    fake = [
        { "projected": 20,  "actual": 13,},
        { "projected": 20,  "actual": 1,},
        { "projected": 18,  "actual": 7,},
        { "projected": 20,  "actual": 13,},
    ]
    bias_result = bias(fake)
    assert bias_result == 11



def test_bias_cancels_mixed_misses():
    # Bias lets over- and under-projections cancel; MAE does not.
    # Guards against bias accidentally using abs() and becoming MAE.
    fake = [
            { "projected": 20,  "actual": 15,},
            { "projected": 20,  "actual": 25,},
        ]

    bias_result = bias(fake)
    mae_result = mae(fake)
    assert bias_result == 0 
    assert mae_result == 5