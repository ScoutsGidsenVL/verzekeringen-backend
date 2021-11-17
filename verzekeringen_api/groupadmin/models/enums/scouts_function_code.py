class ScoutsFunctionCode:

    GROUP_LEADER = "GRL"
    ADJUNCT_GROUP_LEADER = "AGRL"
    GROUP_LEADER_TEAM = "GRLP"

    DISTRICT_COMMISSIONER = "DC"
    ADJUNCT_DISCTRICT_COMMISSIONER = "ADC"
    DISTRICT_COMMISSIONER_TEAM = "DPL"

    LEADER = ""

    MATERIAL_MASTER = "MM"

    UNKNOWN = ""

    code: str

    def __init__(self, code: str = None):
        if not code or len(code) == 0:
            code = self.UNKNOWN
        self.code = code

    def is_district_commissioner(self):
        return self in (
            self.DISTRICT_COMMISSIONER,
            self.ADJUNCT_DISCTRICT_COMMISSIONER,
            self.DISTRICT_COMMISSIONER_TEAM,
        )

    def is_group_leader(self):
        return self in (self.GROUP_LEADER, self.ADJUNCT_GROUP_LEADER, self.GROUP_LEADER_TEAM)

    def is_leader(self):
        return self in (self.LEADER)
