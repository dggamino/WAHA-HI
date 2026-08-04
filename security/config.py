"""
Security configuration.
"""

API_KEYS = {

    "demo-key-001":
    "internal"

}


def validate_key(api_key):

    return API_KEYS.get(
        api_key
    )
