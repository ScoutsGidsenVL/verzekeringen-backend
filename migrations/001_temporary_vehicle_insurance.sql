alter table vrzktypetijdauto
	add inuits_vehicle_id int default NULL;

alter table vrzktypetijdauto
	add constraint vrzktypetijdauto_equipment_inuitsvehicle_id_fk
		foreign key (inuits_vehicle_id) references equipment_inuitsvehicle
			on delete cascade;