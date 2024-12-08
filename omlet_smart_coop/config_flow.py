import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_HOST

from .const import DOMAIN, WEBHOOK_TOKEN


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
                vol.Required(
                    CONF_API_KEY,
                    msg="API Key",
                    description={
                        "friendly_name": "API Key",
                        "description": "Create a key at https://smart.omlet.com/developers",
                    },
                ): str,
                vol.Optional(
                    WEBHOOK_TOKEN,
                    msg="Webhook Token",
                    description={
                        "friendly_name": "Webhook Token",
                        "description": "An optional token to verify the validity of the webhook",
                    },
                ): str,
                vol.Optional(
                    CONF_HOST,
                    default="https://x107.omlet.co.uk",
                    description={
                        "friendly_name": "Host",
                        "description": "Optional custom host address",
                    },
                ): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema)
