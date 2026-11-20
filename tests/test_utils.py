from datetime import date, datetime, timezone

from scouts_auth.inuits.utils import DateUtils
from scouts_insurances.insurances.utils import InsuranceAttachmentUtils


def test_datetime_from_isoformat_negeert_fracties_en_leest_z_als_utc():
    resultaat = DateUtils.datetime_from_isoformat("2026-11-20T14:30:15.123Z")

    assert resultaat == datetime(2026, 11, 20, 14, 30, 15, tzinfo=timezone.utc)


def test_date_from_isoformat():
    assert DateUtils.date_from_isoformat("2026-11-20T14:30:15+01:00") == date(2026, 11, 20)
    assert DateUtils.date_from_isoformat(None) is None


def test_generate_attachment_file_name():
    zonder_suffix = InsuranceAttachmentUtils.generate_attachment_file_name(
        42, "schadeaangiftes/", "schadeaangifte", ".pdf"
    )
    met_suffix = InsuranceAttachmentUtils.generate_attachment_file_name(
        42, "schadeaangiftes/", "schadeaangifte", ".pdf", suffix="bijlage"
    )

    assert zonder_suffix == "schadeaangiftes/schadeaangifte_0000000042.pdf"
    assert met_suffix == "schadeaangiftes/schadeaangifte_0000000042_bijlage.pdf"
