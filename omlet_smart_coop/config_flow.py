import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_HOST

from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class OmletConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Omlet."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Omlet Coop", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_HOST, default="https://x107.omlet.co.uk"): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema)
