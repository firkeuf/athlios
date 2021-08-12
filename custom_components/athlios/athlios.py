from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import HomeAssistantError
import async_timeout


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


async def async_get(hass: HomeAssistant, host: str, path: str, protocol: str) -> dict:
    url = '{0}://{1}{2}'.format(protocol, host, path)
    websession = async_get_clientsession(hass)
    try:
        with async_timeout.timeout(10):
            resp = await websession.get(url)
        json_response = await resp.json()
    except:
        raise CannotConnect
    return json_response
