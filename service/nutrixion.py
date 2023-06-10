

from core.exceptions import ValidationError
from core.configvars import env_config
import httpx
import json

def get_nutrition_data(text):
    headers = {"x-app-id": f"{env_config.NUTRIXION_APP_ID}", "x-app-key": f"{env_config.NUTRIXION_APP_KEY}"}
    url = f"{env_config.URL}?query={text}"
    timeout = httpx.Timeout(None, read=5.0)
    resp: httpx.Response = httpx.get(url, headers=headers, timeout=timeout)
    if resp.status_code != 200:
        msg = json.loads(resp.text).get("message")
        raise ValidationError(detail=msg)
    data = resp.json()

    food = data.get('branded')[0]
    number_of_calories = food.get("nf_calories")

    return number_of_calories