"""Data update coordinator for KACO Inverter."""
from __future__ import annotations

import logging
import socket
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DATA_AUTH,
    DATA_PACKETS,
    SOCKET_TIMEOUT_AUTH,
    SOCKET_TIMEOUT_DATA,
    SOCKET_BUFFER_SIZE,
    DEFAULT_UPDATE_INTERVAL,
    MQTT_TOPICS,
    CONF_INVERTER_HOST,
    CONF_INVERTER_PORT,
    CONF_UPDATE_INTERVAL,
    CONF_MQTT_ENABLED,
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    CONF_MQTT_USERNAME,
    CONF_MQTT_PASSWORD,
)
from .parser import parse_inverter_data

_LOGGER = logging.getLogger(__name__)


class KacoInverterCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator that polls the KACO inverter and parses the response."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        """Initialize the coordinator."""
        interval = config.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )
        self._host: str = config[CONF_INVERTER_HOST]
        self._port: int = config[CONF_INVERTER_PORT]
        self._mqtt_enabled: bool = config.get(CONF_MQTT_ENABLED, False)
        self._mqtt_config: dict | None = None
        if self._mqtt_enabled:
            self._mqtt_config = {
                "host": config[CONF_MQTT_HOST],
                "port": config.get(CONF_MQTT_PORT, 1883),
                "username": config.get(CONF_MQTT_USERNAME),
                "password": config.get(CONF_MQTT_PASSWORD),
            }
        self._previous_data: dict = {}

    async def _async_update_data(self) -> dict:
        """Fetch and parse data from the KACO inverter."""
        try:
            hex_data = await self.hass.async_add_executor_job(self._fetch_data)
        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with KACO inverter at {self._host}:{self._port}: {err}"
            ) from err

        parsed = parse_inverter_data(hex_data)

        # Merge with previous data so values persist across polls
        self._previous_data.update(parsed)
        data = dict(self._previous_data)

        # Compute derived values
        self._compute_derived(data)

        # Optionally publish to MQTT
        if self._mqtt_enabled and self._mqtt_config:
            try:
                await self.hass.async_add_executor_job(self._publish_mqtt, data)
            except Exception:
                _LOGGER.exception("Failed to publish KACO data to MQTT")

        return data

    def _fetch_data(self) -> str:
        """Connect to the inverter, send all packets, return combined hex response."""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.settimeout(10)
            client.connect((self._host, self._port))

            # Authentication handshake
            client.send(bytes.fromhex(DATA_AUTH))
            client.settimeout(SOCKET_TIMEOUT_AUTH)
            combined = client.recv(SOCKET_BUFFER_SIZE)

            # Send all data request packets and collect responses
            for packet in DATA_PACKETS:
                client.send(bytes.fromhex(packet))
                client.settimeout(SOCKET_TIMEOUT_DATA)
                try:
                    response = client.recv(SOCKET_BUFFER_SIZE)
                    if response:
                        combined += response
                except OSError:
                    continue

            return combined.hex()
        finally:
            client.close()

    @staticmethod
    def _compute_derived(data: dict) -> None:
        """Compute derived values in-place from raw parsed data."""
        # Inverter total power
        inv_keys = ("power_inv_l1", "power_inv_l2", "power_inv_l3")
        if all(k in data for k in inv_keys):
            data["power_inv_total"] = (
                data["power_inv_l1"] + data["power_inv_l2"] + data["power_inv_l3"]
            )

        # Net total power
        net_keys = ("power_net_l1", "power_net_l2", "power_net_l3")
        if all(k in data for k in net_keys):
            data["power_net_total"] = (
                data["power_net_l1"] + data["power_net_l2"] + data["power_net_l3"]
            )

        # Consumption = inverter power + net power (per phase)
        all_phase_keys = inv_keys + net_keys
        if all(k in data for k in all_phase_keys):
            data["power_sum_cons"] = (
                (data["power_inv_l1"] + data["power_net_l1"])
                + (data["power_inv_l2"] + data["power_net_l2"])
                + (data["power_inv_l3"] + data["power_net_l3"])
            )

        # Real net grid consumption (consumption - feed in)
        if "today_cons_from_grid" in data and "today_grid_feed_in" in data:
            data["real_grid_feed_in_today"] = round(
                data["today_cons_from_grid"] - data["today_grid_feed_in"], 1
            )

        if "this_month_cons_from_grid" in data and "this_month_grid_feed_in" in data:
            data["real_grid_feed_in_month"] = round(
                data["this_month_cons_from_grid"] - data["this_month_grid_feed_in"], 1
            )

    def _publish_mqtt(self, data: dict) -> None:
        """Publish sensor values to MQTT broker (blocking)."""
        import paho.mqtt.publish as mqtt_publish
        from paho.mqtt.enums import MQTTProtocolVersion

        msgs = []
        for key, topic in MQTT_TOPICS.items():
            value = data.get(key)
            if value is not None:
                msgs.append({"topic": topic, "payload": str(value)})

        if not msgs or not self._mqtt_config:
            return

        auth = None
        if self._mqtt_config.get("username"):
            auth = {
                "username": self._mqtt_config["username"],
                "password": self._mqtt_config.get("password", ""),
            }

        mqtt_publish.multiple(
            msgs,
            hostname=self._mqtt_config["host"],
            port=self._mqtt_config["port"],
            protocol=MQTTProtocolVersion.MQTTv5,
            auth=auth,
        )
