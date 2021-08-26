alter table vrzknietleden
	add inuits_non_member_id int;

alter table vrzknietleden
	add constraint vrzknietleden_members_inuitsnonmember_id_fk
		foreign key (inuits_non_member_id) references members_inuitsnonmember;
