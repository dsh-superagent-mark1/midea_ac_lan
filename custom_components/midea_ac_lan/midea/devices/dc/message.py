from ...core.message import (
    MessageType,
    MessageRequest,
    MessageResponse,
    MessageBody,
)

# Program (drying mode) values, mirrored from the device's own Lua protocol
# table (report/control mapping byte 15), range 0x00..0x31.
DRYER_PROGRAMS = {
    "cotton": 0x00,
    "fiber": 0x01,
    "mixed_wash": 0x02,
    "jean": 0x03,
    "bedsheet": 0x04,
    "outdoor": 0x05,
    "down_jacket": 0x06,
    "plush": 0x07,
    "wool": 0x08,
    "dehumidify": 0x09,
    "cold_air_fresh_air": 0x0A,
    "hot_air_dry": 0x0B,
    "sport_clothes": 0x0C,
    "underwear": 0x0D,
    "baby_clothes": 0x0E,
    "shirt": 0x0F,
    "standard": 0x10,
    "quick_dry": 0x11,
    "fresh_air": 0x12,
    "low_temp_dry": 0x13,
    "eco_dry": 0x14,
    "quick_dry_30": 0x15,
    "towel": 0x16,
    "intelligent_dry": 0x17,
    "steam_care": 0x18,
    "big": 0x19,
    "fixed_time_dry": 0x1A,
    "night_dry": 0x1B,
    "bracket_dry": 0x1C,
    "western_trouser": 0x1D,
    "dehumidification": 0x1E,
    "smart_dry": 0x1F,
    "four_piece_suit": 0x20,
    "warm_clothes": 0x21,
    "quick_dry_20": 0x22,
    "steam_sterilize": 0x23,
    "enzyme": 0x24,
    "big_60": 0x25,
    "steam_no_iron": 0x26,
    "air_wash": 0x27,
    "bed_clothes": 0x28,
    "little_fast_dry": 0x29,
    "small_piece_dry": 0x2A,
    "big_dry": 0x2B,
    "wool_nurse": 0x2C,
    "sun_quilt": 0x2D,
    "fresh_remove_smell": 0x2E,
    "bucket_self_clean": 0x2F,
    "silk": 0x30,
    "sterilize": 0x31,
}
PROGRAM_BY_VALUE = {v: k for k, v in DRYER_PROGRAMS.items()}

RUNNING_STATUS = {
    1: "standby",
    2: "start",
    3: "pause",
    4: "end",
    5: "prevent_wrinkle_end",
    6: "delay_choosing",
    7: "fault",
    8: "delay",
    9: "delay_pause",
}


class MessageDCBase(MessageRequest):
    def __init__(self, protocol_version, message_type, body_type):
        super().__init__(
            device_type=0xDC,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type
        )

    @property
    def _body(self):
        raise NotImplementedError


class MessageQuery(MessageDCBase):
    def __init__(self, protocol_version):
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=0x03)

    @property
    def _body(self):
        return bytearray([])


class MessagePower(MessageDCBase):
    def __init__(self, protocol_version):
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=0x02)
        self.power = False

    @property
    def _body(self):
        power = 0x01 if self.power else 0x00
        return bytearray([
            power, 0xFF
        ])


class MessageStart(MessageDCBase):
    """Start / stop the dryer, optionally selecting a drying program.

    Wire layout (1-based byte index over the full AA frame):
      byte 12 = power
      byte 13 = control_status (0x01 start / 0x00 pause)
      byte 14 = reserved (0xFF)
      byte 15 = program  <-- selected drying mode
    midea_ac_lan builds the frame as body_type + _body, so _body[0] maps to
    byte 12 and the program lives at _body[3].
    """

    def __init__(self, protocol_version):
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=0x02)
        self.start = False
        self.power = True
        self.program = None
        self.washing_data = bytearray([])

    @property
    def _body(self):
        data = bytearray(self.washing_data) if self.washing_data else bytearray([])
        if len(data) < 4:
            data = bytearray([0xFF, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                              0xFF, 0xFF, 0xFF, 0xFF])
        if self.program is not None:
            data[1] = self.program & 0xFF
        data[0] = 0xFF
        if self.start:
            return bytearray([0xFF, 0x01]) + data
        else:
            return bytearray([0xFF, 0x00]) + data


class DCGeneralMessageBody(MessageBody):
    def __init__(self, body):
        super().__init__(body)
        # body[0] is the body type; field bytes start at body[1].
        self.power = body[1] > 0
        self.running_status = RUNNING_STATUS.get(body[2], "unknown")
        self.start = body[2] in [2, 6]
        self.washing_data = body[3:15]
        if len(body) > 4:
            self.program = PROGRAM_BY_VALUE.get(body[4], f"program_{body[4]:02X}")
        else:
            self.program = None
        self.progress = 0
        for i in range(0, 7):
            if (body[16] & (1 << i)) > 0:
                self.progress = i + 1
                break
        if self.power:
            self.time_remaining = body[17] + body[18] * 60
        else:
            self.time_remaining = None


class MessageDCResponse(MessageResponse):
    def __init__(self, message):
        super().__init__(message)
        if self.message_type in [MessageType.query, MessageType.set] or \
                (self.message_type == MessageType.notify1 and self.body_type == 0x04):
            self.set_body(DCGeneralMessageBody(super().body))
        self.set_attr()
