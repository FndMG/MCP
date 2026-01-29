import httpx
import logging
import json
from typing import Dict, Any
from config.config import Config

def log_requests_and_response(response: httpx.Response):
    try:
        req = response.request
        body_content = req.content if req.body else "None"

        logging.debug("--- HTTP Request Details ---")
        logging.debug(f"URL: {req.url}")
        logging.debug(f"METHOD: {req.method}")
        logging.debug(f"HEADERS: {dict(req.headers)}")
        logging.debug(f"BODY: {body_content}")
    except Exception as e:
        logging.warning(f"Error logging request: {e}")

    try:
        response_data = response.text

        try:
            response_json = response.json()
            response_data = json.dumps(response_json, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass

        logging.debug("--- HTTP Response Details ---")
        logging.debug(f"STATUS: {response.status_code}")
        logging.debug(f"REASON: {response.reason_phrase}")
        logging.debug(f"HEADERS: {dict(response.headers)}")
        logging.debug(f"CONTENT: \n{response_data}")
        logging.debug("------------------------------")

    except Exception as e:
        logging.warning(f"Error logging response: {e}")


async def call_api(api_url: str, params: Dict[str, Any] = None, http_method: str = "GET") -> Dict[str, Any]:
    try:
        http_method = http_method.upper()

        async with httpx.AsyncClient(timeout=Config.TIME_OUT_SECONDS) as client:
            response = await client.request(
                http_method,
                api_url,
                params=params if http_method == "GET" or http_method == "DELETE" else None,
                json=params if http_method in ["POST", "PUT", "PATCH"] else None,
                cookies=None,
                headers=None, #TODO: 未実装
            )

        log_requests_and_response(response)
        response.raise_for_status()
        return response.json()

    except httpx.RequestError as e:
        error_message = f"API request error ({api_url}): {e}"
        logging.error(error_message)
        return {"status": "error", "message": error_message}
