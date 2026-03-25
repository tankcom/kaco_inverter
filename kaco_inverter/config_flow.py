"""Config flow for KACO Inverter integration."""
from __future__ import annotations

import socket

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DEFAULT_INVERTER_PORT,
    DEFAULT_MQTT_PORT,
    DEFAULT_UPDATE_INTERVAL,
    CONF_INVERTER_HOST,
    CONF_INVERTER_PORT,
    CONF_UPDATE_INTERVAL,
    CONF_MQTT_ENABLED,
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    CONF_MQTT_USERNAME,
    CONF_MQTT_PASSWORD,
)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_INVERTER_HOST): str,
        vol.Required(CONF_INVERTER_PORT, default=DEFAULT_INVERTER_PORT): int,
        vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(
            int, vol.Range(min=1, max=3600)
        ),
        vol.Required(CONF_MQTT_ENABLED, default=False): bool,
    }
)

STEP_MQTT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MQTT_HOST): str,
        vol.Required(CONF_MQTT_PORT, default=DEFAULT_MQTT_PORT): int,
        vol.Required(CONF_MQTT_USERNAME): str,
        vol.Required(CONF_MQTT_PASSWORD): str,
    }
)


class KacoInverterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for KACO Inverter."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: dict = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> KacoInverterOptionsFlow:
        """Return the options flow handler."""
        return KacoInverterOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the inverter connection step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_INVERTER_HOST]
            port = user_input[CONF_INVERTER_PORT]

            can_connect = await self.hass.async_add_executor_job(
                _test_connection, host, port
            )

            if can_connect:
                self._data.update(user_input)

                await self.async_set_unique_id(f"kaco_{host}_{port}")
                self._abort_if_unique_id_configured()

                if user_input.get(CONF_MQTT_ENABLED):
                    return await self.async_step_mqtt()

                return self.async_create_entry(
                    title=f"KACO Inverter ({host})",
                    data=self._data,
                )

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )

    async def async_step_mqtt(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the MQTT configuration step."""
        if user_input is not None:
            self._data.update(user_input)
            host = self._data[CONF_INVERTER_HOST]
            return self.async_create_entry(
                title=f"KACO Inverter ({host})",
                data=self._data,
            )

        return self.async_show_form(
            step_id="mqtt",
            data_schema=STEP_MQTT_SCHEMA,
        )


class KacoInverterOptionsFlow(config_entries.OptionsFlow):
    """Handle options for an existing KACO Inverter config entry."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self._config_entry = config_entry
        self._data: dict = dict(config_entry.data)

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """First step: inverter connection + general settings."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_INVERTER_HOST]
            port = user_input[CONF_INVERTER_PORT]

            can_connect = await self.hass.async_add_executor_job(
                _test_connection, host, port
            )

            if can_connect:
                self._data.update(user_input)

                if user_input.get(CONF_MQTT_ENABLED):
                    return await self.async_step_mqtt()

                # Clear MQTT fields if MQTT was disabled
                for key in (CONF_MQTT_HOST, CONF_MQTT_PORT, CONF_MQTT_USERNAME, CONF_MQTT_PASSWORD):
                    self._data.pop(key, None)

                self.hass.config_entries.async_update_entry(
                    self._config_entry, data=self._data
                )
                return self.async_create_entry(title="", data={})

            errors["base"] = "cannot_connect"

        cur = self._data
        schema = vol.Schema(
            {
                vol.Required(CONF_INVERTER_HOST, default=cur.get(CONF_INVERTER_HOST, "")): str,
                vol.Required(CONF_INVERTER_PORT, default=cur.get(CONF_INVERTER_PORT, DEFAULT_INVERTER_PORT)): int,
                vol.Required(CONF_UPDATE_INTERVAL, default=cur.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)): vol.All(
                    int, vol.Range(min=1, max=3600)
                ),
                vol.Required(CONF_MQTT_ENABLED, default=cur.get(CONF_MQTT_ENABLED, False)): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_mqtt(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """MQTT configuration step."""
        if user_input is not None:
            self._data.update(user_input)
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=self._data
            )
            return self.async_create_entry(title="", data={})

        cur = self._data
        schema = vol.Schema(
            {
                vol.Required(CONF_MQTT_HOST, default=cur.get(CONF_MQTT_HOST, "")): str,
                vol.Required(CONF_MQTT_PORT, default=cur.get(CONF_MQTT_PORT, DEFAULT_MQTT_PORT)): int,
                vol.Required(CONF_MQTT_USERNAME, default=cur.get(CONF_MQTT_USERNAME, "")): str,
                vol.Required(CONF_MQTT_PASSWORD, default=cur.get(CONF_MQTT_PASSWORD, "")): str,
            }
        )

        return self.async_show_form(
            step_id="mqtt",
            data_schema=schema,
        )


def _test_connection(host: str, port: int) -> bool:
    """Test TCP connection to the inverter."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        sock.close()
        return True
    except OSError:
        return False
