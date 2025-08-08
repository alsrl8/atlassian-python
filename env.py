import os

domain = os.getenv("DOMAIN")
email = os.getenv("EMAIL")
api_token = os.getenv("API_TOKEN")

if domain is None:
    print("`DOMAIN` environment variable is not set.")
    exit(1)
if email is None:
    print("`EMAIL` environment variable is not set.")
    exit(1)
if api_token is None:
    print("`API_TOKEN` environment variable is not set.")
    exit(1)


def get_domain():
    return domain


def get_email():
    return email


def get_api_token():
    return api_token
