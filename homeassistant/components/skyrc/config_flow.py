"""Config flow for SkyRC."""
from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN


class SkyRcConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SkyRC."""
