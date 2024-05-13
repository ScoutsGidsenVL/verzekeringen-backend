base_insurance_fields = [
    # id                    pk
    "id",
    # _status               number          optional
    "status",
    # don't serialize invoice_number to clients
    # invoice_number        number          optional
    # don't serialize invoice_date to clients
    # invoice_date          date            optional
    # getter and setter on BaseInsurance for scouts_group
    # _group_group_admin_id max_length=6    required
    # _group_name           max_length=50   required
    # _group_location       max_length=50   required
    # _group_group_admin_id, _group_name, _group_location are serialized as a AbstractScoutsGroup instance
    "scouts_group",
    # total_cost            decimal         optional
    "total_cost",
    # comment               max_length=500  optional
    "comment",
    # vvksm_comment         max_length=500  optional
    "vvksm_comment",
    # _printed              max_length=1    optional, default="N"
    # _finished             max_length=1    optional, default="N"
    # _listed               max_length=1    optional, default="N"
    # created_on            datetime        optional
    "created_on",
    # _start_date           datetime        optional
    "start_date",
    # _end_date             datetime        optional
    "end_date",
    # payment_date          datetime        optional
    # responsible_member    Member          required
    "responsible_member",
    # type                  InsuranceType   optional
    # "type",
]
