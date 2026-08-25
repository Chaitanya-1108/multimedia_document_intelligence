from app.url_extraction.url_model import URLData


def test_url_data_stores_extracted_url_information():
    result = URLData(
        url="https://example.com/login",
        domain="example.com",
        start=11,
        end=35,
    )

    assert result.url == "https://example.com/login"
    assert result.domain == "example.com"
    assert result.start == 11
    assert result.end == 35


def test_url_data_is_immutable():
    result = URLData(
        url="https://example.com",
        domain="example.com",
        start=0,
        end=19,
    )

    try:
        result.url = "https://changed.com"
        assert False, "URLData should be immutable"
    except AttributeError:
        pass