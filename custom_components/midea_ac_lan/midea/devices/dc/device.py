import logging
from .message import (
    DRYER_PROGRAMS,
    PROGRAM_LABELS_EN,
    PROGRAM_LABELS_ZH,
    PROGRAM_BY_VALUE,
    MessageQuery,
    MessagePower,
    MessageStart,
    MessageDCResponse
)
try:
    from enum import StrEnum
except ImportError:
    from ...backports.enum import StrEnum
from ...core.device import MiedaDevice

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    power = "power"
    start = "start"
    program = "program"
    running_status = "running_status"
    washing_data = "washing_data"
    progress = "progress"
    time_remaining = "time_remaining"


class MideaDADevice(MiedaDevice):
    def __init__(
            self,
            name: str,
            device_id: int,
            ip_address: str,
            port: int,
            token: str,
            key: str,
            protocol: int,
            model: str,
            subtype: int,
            customize: str
    ):
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=0xDC,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.start: False,
                DeviceAttributes.program: "unknown",
                DeviceAttributes.running_status: "unknown",
                DeviceAttributes.washing_data: bytearray([]),
                DeviceAttributes.progress: "Unknown",
                DeviceAttributes.time_remaining: None
            })

    @property
    def preset_modes(self):
        """All program keys supported by the dryer (protocol values)."""
        return list(DRYER_PROGRAMS.keys())

    @property
    def program_labels(self):
        """Program key -> display name, localised to the HA language."""
        lang = getattr(self, "hass_language", None) or "en"
        table = PROGRAM_LABELS_ZH if str(lang).lower().startswith("zh") \
            else PROGRAM_LABELS_EN
        return table

    def build_query(self):
        return [MessageQuery(self._protocol_version)]

    def process_message(self, msg):
        message = MessageDCResponse(msg)
        _LOGGER.debug(f"[{self.device_id}] Received: {message}")
        new_status = {}
        progress = ["Prog0", "Prog1", "Prog2", "Prog3",
                    "Prog4", "Prog5", "Prog6", "Prog7"]
        for status in self._attributes.keys():
            if hasattr(message, str(status)):
                if status == DeviceAttributes.progress:
                    self._attributes[status] = progress[getattr(message, str(status))]
                else:
                    self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr, value):
        if attr == DeviceAttributes.power:
            message = MessagePower(self._protocol_version)
            message.power = value
            self.build_send(message)
        elif attr == DeviceAttributes.program:
            # Selecting a program must reach the device, otherwise the next
            # status refresh restores the old value. Send a SET frame that
            # keeps the current run/pause state but carries the new program.
            self._attributes[DeviceAttributes.program] = value
            message = MessageStart(self._protocol_version)
            is_running = self._attributes.get(DeviceAttributes.running_status) in (
                "start", "pause") or self._attributes.get(DeviceAttributes.start)
            message.start = bool(is_running)
            message.washing_data = self._attributes[DeviceAttributes.washing_data]
            message.program = DRYER_PROGRAMS.get(value) if isinstance(value, str) else None
            self.build_send(message)
        elif attr == DeviceAttributes.start:
            message = MessageStart(self._protocol_version)
            message.start = value
            message.washing_data = self._attributes[DeviceAttributes.washing_data]
            current = self._attributes.get(DeviceAttributes.program)
            message.program = DRYER_PROGRAMS.get(current) if isinstance(current, str) else None
            self.build_send(message)

    def start_with_program(self, value: bool, program: str = None):
        """Start/stop the dryer with an explicit program name."""
        message = MessageStart(self._protocol_version)
        message.start = value
        message.washing_data = self._attributes[DeviceAttributes.washing_data]
        if program is not None and program in DRYER_PROGRAMS:
            message.program = DRYER_PROGRAMS[program]
            self._attributes[DeviceAttributes.program] = program
        self.build_send(message)


class MideaAppliance(MideaDADevice):
    pass
