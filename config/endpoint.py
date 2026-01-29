from os import getenv
from dotenv import load_dotenv

load_dotenv()


class ApiEndpoints:
    PROTOCOL = getenv("PROTOCOL", "http")
    API_HOST_NAME = getenv("API_HOST_NAME")
    API_PATH = getenv("API_PATH")

    if API_HOST_NAME and not API_HOST_NAME.startswith("http"):
        API_BASE_URL = f"{PROTOCOL}://{API_HOST_NAME}"
    else:
        API_BASE_URL = API_HOST_NAME

    API_ROOT_URL = f"{API_BASE_URL}/{API_PATH}"

    LOGIN_URL = f"{API_BASE_URL}/login"
    LOGOUT_URL = f"{API_BASE_URL}/logout"

    TEMPLATE_LIST_URL = f"{API_BASE_URL}/templates"
    TEMPLATE_DETAIL_URL = f"{API_BASE_URL}/templates"
