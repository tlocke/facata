from facata.utils import to_pyformat


def test_to_pyformat():
    actual = to_pyformat("SELECT :value")

    assert actual == "SELECT %(value)s"
