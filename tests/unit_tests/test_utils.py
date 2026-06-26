from src.utils.utils import read_file


def test_read_file():
    test_data_exmp = {
        "title": "Bridge Resort",
        "location": "посёлок городского типа Сириус, Фигурная улица, 45",
    }
    path = "tests/mock_hotels.json"
    data = read_file(path)

    assert data
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert data[-1] == test_data_exmp
