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

# Localised program names (zh / en). Kept in step with
# translations/*.json -> entity.select.dryer_program.state.
PROGRAM_LABELS_ZH = {
    "cotton": "棉织物",
    "fiber": "化纤",
    "mixed_wash": "混合",
    "jean": "牛仔",
    "bedsheet": "床单",
    "outdoor": "户外",
    "down_jacket": "羽绒服",
    "plush": "毛绒",
    "wool": "羊毛",
    "dehumidify": "除湿",
    "cold_air_fresh_air": "冷风清新",
    "hot_air_dry": "热风烘干",
    "sport_clothes": "运动服",
    "underwear": "内衣",
    "baby_clothes": "婴儿衣物",
    "shirt": "衬衫",
    "standard": "标准",
    "quick_dry": "快速烘干",
    "fresh_air": "清新空气",
    "low_temp_dry": "低温烘干",
    "eco_dry": "节能烘干",
    "quick_dry_30": "快速烘干30分",
    "towel": "毛巾",
    "intelligent_dry": "智能烘干",
    "steam_care": "蒸汽护理",
    "big": "大件",
    "fixed_time_dry": "定时烘干",
    "night_dry": "夜间烘干",
    "bracket_dry": "衣架烘干",
    "western_trouser": "西裤",
    "dehumidification": "除湿",
    "smart_dry": "智慧烘干",
    "four_piece_suit": "四件套",
    "warm_clothes": "暖衣",
    "quick_dry_20": "快速烘干20分",
    "steam_sterilize": "蒸汽除菌",
    "enzyme": "酵素",
    "big_60": "大件60分",
    "steam_no_iron": "蒸汽免熨",
    "air_wash": "空气洗",
    "bed_clothes": "床品",
    "little_fast_dry": "小件快烘",
    "small_piece_dry": "小件烘干",
    "big_dry": "大件烘干",
    "wool_nurse": "羊毛护理",
    "sun_quilt": "晒被",
    "fresh_remove_smell": "清新去味",
    "bucket_self_clean": "滤网自清洁",
    "silk": "丝绸",
    "sterilize": "除菌",
}

PROGRAM_LABELS_EN = {
    "cotton": "Cotton",
    "fiber": "Fiber",
    "mixed_wash": "Mixed Wash",
    "jean": "Jean",
    "bedsheet": "Bedsheet",
    "outdoor": "Outdoor",
    "down_jacket": "Down Jacket",
    "plush": "Plush",
    "wool": "Wool",
    "dehumidify": "Dehumidify",
    "cold_air_fresh_air": "Cold Air Fresh",
    "hot_air_dry": "Hot Air Dry",
    "sport_clothes": "Sport Clothes",
    "underwear": "Underwear",
    "baby_clothes": "Baby Clothes",
    "shirt": "Shirt",
    "standard": "Standard",
    "quick_dry": "Quick Dry",
    "fresh_air": "Fresh Air",
    "low_temp_dry": "Low Temp Dry",
    "eco_dry": "Eco Dry",
    "quick_dry_30": "Quick Dry 30min",
    "towel": "Towel",
    "intelligent_dry": "Intelligent Dry",
    "steam_care": "Steam Care",
    "big": "Big",
    "fixed_time_dry": "Fixed Time Dry",
    "night_dry": "Night Dry",
    "bracket_dry": "Bracket Dry",
    "western_trouser": "Western Trouser",
    "dehumidification": "Dehumidification",
    "smart_dry": "Smart Dry",
    "four_piece_suit": "Four Piece Suit",
    "warm_clothes": "Warm Clothes",
    "quick_dry_20": "Quick Dry 20min",
    "steam_sterilize": "Steam Sterilize",
    "enzyme": "Enzyme",
    "big_60": "Big 60min",
    "steam_no_iron": "Steam No Iron",
    "air_wash": "Air Wash",
    "bed_clothes": "Bed Clothes",
    "little_fast_dry": "Little Fast Dry",
    "small_piece_dry": "Small Piece Dry",
    "big_dry": "Big Dry",
    "wool_nurse": "Wool Nurse",
    "sun_quilt": "Sun Quilt",
    "fresh_remove_smell": "Fresh Remove Smell",
    "bucket_self_clean": "Filter Self Clean",
    "silk": "Silk",
    "sterilize": "Sterilize",
}


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
        # MessageRequest.body prepends the body_type, so _body[0] lands on
        # frame byte 12: _body[0]=power, [1]=control_status, [2]=reserved,
        # [3]=program, then the remaining washing-data tail (wd[2:]).
        wd = bytearray(self.washing_data) if self.washing_data else bytearray([])
        tail = bytearray(wd[2:]) if len(wd) > 2 else bytearray([])
        if len(tail) < 10:
            tail = bytearray([0x0A, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00,
                              0x00, 0x00])
        program = self.program if self.program is not None else (wd[1] if len(wd) > 1 else 0x00)
        body = bytearray([
            0xFF,                                   # power (forced on)
            0x01 if self.start else 0x00,           # control_status
            0xFF,                                   # reserved
            program & 0xFF,                         # program
        ])
        return body + tail


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
