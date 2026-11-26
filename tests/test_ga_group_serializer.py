from scouts_auth.groupadmin.serializers import AbstractScoutsGroupSerializer


def test_groepsnummer_wordt_group_admin_id_bij_technische_sleutel():
    for technische_sleutel in ("d5f75b320b812440010b81254662006a", "MERGE_2016_d5f75b320b812440010b81254e780212"):
        data = AbstractScoutsGroupSerializer().to_internal_value({"id": technische_sleutel, "groepsnummer": "A1234G"})

        assert data["group_admin_id"] == "A1234G"
        assert data["number"] == "A1234G"


def test_id_blijft_behouden_zonder_groepsnummer():
    data = AbstractScoutsGroupSerializer().to_internal_value({"id": "A1234G"})

    assert data["group_admin_id"] == "A1234G"
    assert data["number"] is None
