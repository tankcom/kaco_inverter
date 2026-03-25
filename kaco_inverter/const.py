"""Constants for the KACO Inverter integration."""

DOMAIN = "kaco_inverter"

DEFAULT_INVERTER_PORT = 9760
DEFAULT_MQTT_PORT = 1883

CONF_INVERTER_HOST = "inverter_host"
CONF_INVERTER_PORT = "inverter_port"
CONF_MQTT_ENABLED = "mqtt_enabled"
CONF_MQTT_HOST = "mqtt_host"
CONF_MQTT_PORT = "mqtt_port"
CONF_MQTT_USERNAME = "mqtt_username"
CONF_MQTT_PASSWORD = "mqtt_password"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_UPDATE_INTERVAL = 30  # seconds

# Authentication packet
DATA_AUTH = (
    "55aa301300d7080000cc3f0ccfa06dd9576f21239eb0e51190447475"
)

# Data request packets (sent sequentially after authentication)
DATA_PACKETS = [
    "55aa3450000c2a000025a1234b25a1234bbcfc91e598cb97bfa607674005667fc0d9eb9cf27b6352af368e8ded1e1372c04878677886785c7c7b7c9a7c871fa61fc51fbccadbca5396e9d25e89daedd8bee4a003a122a124fa",
    "55aa345000b8260000ff2b67d47b3f340f1fe5d395b4a014e8310b19cf6ebf44fe23da538ebfae4f6a90a5111212f0090d8b8e428e9dcd6dd0aa3a057a9d8849246824fd2de4bf5fb7234b1dcf1ab1b0e449919ee65bb27dfe",
    "55aa341a00ab0d00004b3c51bd4f0cf556f8277ce77020f7d2dda3d4ab012d97dabc3b",
    "55aa343a00c71c000057e671d7ef990e3e5de687761df9b395e58734ad669f380b6afddb9ca9aa058a89c35209582055f9f365da1b74728e4f154d6433768bfa0c718d",
    "55aa345000c7250000256b3454c27c2255c5a094d8269ebc34a7d34a51dc3a6b73fd5cbbe4acdf73e36044ac470f7c5fec1c30a8bc3ae738a5700d02384d14df3ebd8b048076c2240f0e745e0ff3e454cdc9f20b0a9ab7c044",
    "55aa345000f02800007dfe4b3c51bd4f0cf556f8277ce77020f7d2dda3d4ab012d97da71d7ef990e3eb395e58734ad669fdb9ca9aa058a89c35209582055f9f365da1b74728e4f154d6433768bfa0c94d8269ebc34a7d34a51",
    "55aa345000d2240000a9aa058a89c35209582055f9f365da1b74728e4f154dfa0c94d8269ebc34a7d34a51dc3a6b73fd5cbbe4acdf73e36044ac470f7c5fec1c30a8bc3ae738a5700d02384d14df3ebd8b048076c2240f0e74",
    "55aa345000482900005e0ff3e454cdc9f20b0a9ab7c04491afec35308e76881c90d0c435664858923a43711e8c0035ec8ace1cc262a41931c98c78fcb207da8def2fa7e3abbc39e5c31db5cdb4f9fc9d12b53c8612f008cf35",
    "55aa345000cb230000acdf73e36044ac470f7c5fec1c30a8bc3ae738a5700d02384d14df3ebd8b048076c2240f0e745e0ff3e454cdc9f20b0a9ab7c04491afec35308e76881c90d0c435664858923a43711e8c0035ec8ace1c",
    "55aa3450006d2b000090a512f0d9eb538e44fe4f0c428e9dcd6dd0aa3a057a1e1372c0bccadbca4a5191e598cb843150fc885959d26d2f9ab7f3e454cdc9f20b0a058a7dfe3566c0441ab1e4bf5fb7dedb6e65ef2a6afd2cf1",
    "55aa345000e82500007b3f340f1fe5d395b4a014e8310b19cf6ebf44fe23da538ebfae4f6a90a5111212f0090d8b8e428e9dcd6dd0aa3a057a9d8849246824fd2de4bf5fb7234b1dcf1ab1b0e449919ee65bb27dfe4b3c51bd",
    "55aa3440006b20000057e671d7ef990e3e87761df9b395e587058a89c35209582055f9f365da1b74728e4f154dfa0c718d256b3454c27c2255c5a094d8269edc3a6b73fd5cbbe4acdf",
    "55aa34500042260000e587058a89c35209582055f9f365da1b74728e4f154d6433768bfa0c718d256b3454c27c2255c5a094d8269ebc34a7d34a51dc3a6b73fd5cbbe4acdf73e36044ac470f7c5fec1c30a8bc3ae738a5700d",
    "55aa34500091260000cdb4f9fc9d12b53c8612f008cf355a615973e1ef1cdcab65c216bf1f56e9874faeb60f2384adfd2d234b1dcf1ab167d47b3f19cfbfaebc34340f1fe5310bd3955de625a1cdc849246824e4a003a122a1",
    "55aa345000c2270000dedb6e656433768bef2aa7d3380b48786778867853965e895c7c7b7c9a7c90a512f0d9eb538e44fe4f0caa3a057a1e1372c0bccadbca4a5191e598cb843150fc885959d26d2f058a7dfec0441ab15fb7",
    "55aa343a00c71c000057e671d7ef990e3e5de687761df9b395e58734ad669f380b6afddb9ca9aa058a89c35209582055f9f365da1b74728e4f154d6433768bfa0c718d",
]

# Socket timeouts (seconds)
SOCKET_TIMEOUT_AUTH = 4
SOCKET_TIMEOUT_DATA = 1
SOCKET_BUFFER_SIZE = 1024

# MQTT topic mapping (sensor key -> MQTT topic)
MQTT_TOPICS = {
    "power_inv_l1": "kaco/Power_Inv_L1",
    "power_inv_l2": "kaco/Power_Inv_L2",
    "power_inv_l3": "kaco/Power_Inv_L3",
    "power_inv_total": "kaco/Power_Inv_Total",
    "power_net_total": "kaco/Power_Net_Total",
    "u_pv_1": "kaco/U_PV_1",
    "u_pv_2": "kaco/U_PV_2",
    "p_pv": "kaco/P_PV",
    "u_bat": "kaco/U_Bat",
    "p_bat": "kaco/P_Bat",
    "soc_bat": "kaco/SOC_Bat",
    "power_sum_cons": "kaco/power_sum_cons",
    "today_grid_feed_in": "kaco/today_grid_feed_in",
    "this_month_grid_feed_in": "kaco/this_month_grid_feed_in",
    "today_cons_from_grid": "kaco/today_cons_from_grid",
    "this_month_cons_from_grid": "kaco/this_month_cons_from_grid",
    "today_cons_self": "kaco/today_cons_self",
    "this_month_today_cons_self": "kaco/this_month_today_cons_self",
    "today_battery_energy_volume": "kaco/today_battery_energy_volume",
    "this_month_battery_energy_volume": "kaco/this_month_battery_energy_volume",
    "real_grid_feed_in_today": "kaco/real_grid_feed_in_today",
    "real_grid_feed_in_month": "kaco/real_grid_feed_in_month",
    "temp_inverter": "kaco/temp_inverter",
}
