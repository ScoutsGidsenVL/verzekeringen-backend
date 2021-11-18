class ScoutsFunctionCode:

    GROUP_LEADER = "GRL"
    ADJUNCT_GROUP_LEADER = "AGRL"
    GROUP_LEADER_TEAM = "GRLP"

    DISTRICT_COMMISSIONER = "DC"
    ADJUNCT_DISCTRICT_COMMISSIONER = "ADC"
    DISTRICT_COMMISSIONER_TEAM = "DPL"

    SECTION_LEADER = ""

    # MATERIAL_MASTER = "MM"
    # ADJUNCT_MATERIAL_MASTER = "AMM"

    UNKNOWN = ""

    code: str

    def __init__(self, code: str = None):
        if not code or len(code) == 0:
            code = self.UNKNOWN
        self.code = code

    def is_section_leader(self):
        return self in (self.SECTION_LEADER)

    def is_group_leader(self):
        return self in (self.GROUP_LEADER, self.ADJUNCT_GROUP_LEADER, self.GROUP_LEADER_TEAM)

    def is_district_commissioner(self):
        return self in (
            self.DISTRICT_COMMISSIONER,
            self.ADJUNCT_DISCTRICT_COMMISSIONER,
            self.DISTRICT_COMMISSIONER_TEAM,
        )
