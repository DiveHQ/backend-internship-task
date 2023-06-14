from src.core.exceptions import ValidationError, EmptyResponseError
from src.core.configvars import env_config
import httpx
import json
from src.core.exceptions import ErrorResponse
from fastapi import status

def get_nutrition_data(text):
    headers = {
        "x-app-id": f"{env_config.NUTRIXION_APP_ID}",
        "x-app-key": f"{env_config.NUTRIXION_APP_KEY}",
    }
    url = f"{env_config.API_URL}?query={text}"
    timeout = httpx.Timeout(None, read=5.0)
    resp: httpx.Response = httpx.get(url, headers=headers, timeout=timeout)
    if resp.status_code != 200:
        msg = json.loads(resp.text).get("message")
        raise ValidationError(detail=msg)
    data = resp.json()

    branded = data.get("branded")
    if not branded:
        raise ErrorResponse(data=[], errors={"message": env_config.ERRORS.get("ENTRY_NOT_RETRIEVED")}, status_code=status.HTTP_400_BAD_REQUEST)

    food = branded[0]

    number_of_calories = food.get("nf_calories")

    return number_of_calories
