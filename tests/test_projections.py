from projections import score_projection

# Run test .venv/Scripts/python.exe -m pytest


def test_doubtful_is_zeroed():
    fake = [
    {"name": "Test Doubtful", "position": "QB", "espn_projection": 20,
     "status": "DOUBTFUL", "bye": False},
    {"name": "Test Healthy", "position": "QB", "espn_projection": 15,
     "status": "ACTIVE", "bye": False},
]
    result = score_projection(fake)
    assert result[0]["projection"] == 0

    