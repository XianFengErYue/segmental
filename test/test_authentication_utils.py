from authentication.api_key_utils import get_api_key_from_s3


# Assumes AWS Credentials present on system
def test_get_api_key_from_s3_returns_api_key_as_text():
    result = get_api_key_from_s3()

    assert type(result) == str
