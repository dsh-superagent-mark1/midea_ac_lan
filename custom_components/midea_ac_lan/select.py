from .midea_entity import MideaEntity
from .midea_devices import MIDEA_DEVICES
from homeassistant.components.select import SelectEntity
from homeassistant.const import (
    Platform,
    CONF_DEVICE_ID,
    CONF_SWITCHES
)
from .const import (
    DOMAIN,
    DEVICES,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    device_id = config_entry.data.get(CONF_DEVICE_ID)
    device = hass.data[DOMAIN][DEVICES].get(device_id)
    # Let the device localise its option labels to the HA UI language.
    device.hass_language = getattr(hass.config, "language", "en")
    extra_switches = config_entry.options.get(
        CONF_SWITCHES, []
    )
    selects = []
    for entity_key, config in MIDEA_DEVICES[device.device_type]["entities"].items():
        if config["type"] == Platform.SELECT and entity_key in extra_switches:
            dev = MideaSelect(device, entity_key)
            selects.append(dev)
    async_add_entities(selects)


class MideaSelect(MideaEntity, SelectEntity):
    def __init__(self, device, entity_key: str):
        super().__init__(device, entity_key)
        self._options_name = self._config.get("options")
        # Translation key lets HA localise both the entity name and the
        # selectable option labels (entity.select.<key>.state in translations).
        self._attr_translation_key = self._config.get("translation_key")

    @property
    def options(self):
        raw = getattr(self._device, self._options_name)
        labels = getattr(self._device, "program_labels", None)
        if labels and self._config.get("translation_key"):
            return [labels.get(item, item) for item in raw]
        return raw

    @property
    def current_option(self):
        current = self._device.get_attribute(self._entity_key)
        labels = getattr(self._device, "program_labels", None)
        if labels and self._config.get("translation_key"):
            return labels.get(current, current)
        return current

    def select_option(self, option: str):
        # Translate a localised label back to the protocol key.
        labels = getattr(self._device, "program_labels", None)
        if labels:
            inverse = {v: k for k, v in labels.items()}
            option = inverse.get(option, option)
        self._device.set_attribute(self._entity_key, option)
