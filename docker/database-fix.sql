CREATE SEQUENCE auth_group_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
CREATE SEQUENCE auth_group_permissions_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
CREATE SEQUENCE auth_permission_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
CREATE SEQUENCE django_admin_log_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
CREATE SEQUENCE django_content_type_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
CREATE SEQUENCE django_migrations_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.scouts_auth_scoutsuser_groups_id_seq definition 
-- DROP SEQUENCE scouts_auth_scoutsuser_groups_id_seq; 
CREATE SEQUENCE scouts_auth_scoutsuser_groups_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.scouts_auth_scoutsuser_user_permissions_id_seq definition 
-- DROP SEQUENCE scouts_auth_scoutsuser_user_permissions_id_seq; 
CREATE SEQUENCE scouts_auth_scoutsuser_user_permissions_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.scouts_insurances_costvariable_id_seq definition 
-- DROP SEQUENCE scouts_insurances_costvariable_id_seq; 
CREATE SEQUENCE scouts_insurances_costvariable_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.scouts_insurances_country_id_seq definition 
-- DROP SEQUENCE scouts_insurances_country_id_seq; 
CREATE SEQUENCE scouts_insurances_country_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.scouts_insurances_country_insurance_types_id_seq definition 
-- DROP SEQUENCE scouts_insurances_country_insurance_types_id_seq; 
CREATE SEQUENCE scouts_insurances_country_insurance_types_id_seq 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzk_adres definition 
-- DROP SEQUENCE seq_vrzk_adres; 
CREATE SEQUENCE seq_vrzk_adres 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzk_bericht definition 
-- DROP SEQUENCE seq_vrzk_bericht; 
CREATE SEQUENCE seq_vrzk_bericht 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzk_vzw definition 
-- DROP SEQUENCE seq_vrzk_vzw; 
CREATE SEQUENCE seq_vrzk_vzw 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzkleden definition 
-- DROP SEQUENCE seq_vrzkleden; 
CREATE SEQUENCE seq_vrzkleden 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzkmateriaal definition 
-- DROP SEQUENCE seq_vrzkmateriaal; 
CREATE SEQUENCE seq_vrzkmateriaal 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzknietleden definition 
-- DROP SEQUENCE seq_vrzknietleden; 
CREATE SEQUENCE seq_vrzknietleden 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 
-- public.seq_vrzkverzekeringen definition 
-- DROP SEQUENCE seq_vrzkverzekeringen; 
CREATE SEQUENCE seq_vrzkverzekeringen 
MINVALUE 0 
NO MAXVALUE 
START 0 
NO CYCLE; 

CREATE TABLE vrzkverzekeringstypes (
    verzekeringstypeid numeric(2) NOT NULL,
    verzekeringstype varchar(30) NOT NULL,
    verzekeringstypeomschr varchar(70) NOT NULL,
    maxtermijn varchar(10) NOT NULL,
    CONSTRAINT vrzkverzekeringstypes_pkey PRIMARY KEY (verzekeringstypeid)
);

CREATE TABLE public.vrzkleden ( 
    lidid numeric(6) DEFAULT nextval('seq_vrzkleden'::regclass) NOT NULL, 
    naam varchar(60) NOT NULL, 
    voornaam varchar(60) NOT NULL, 
    lidnr numeric(13) NOT NULL, 
    geboortedatum timestamp(6) NULL, 
    telefoon varchar(15) NULL, 
    email varchar(60) NULL, 
    ga_id varchar(255) NULL, 
    CONSTRAINT vrzkleden_check CHECK ((((geboortedatum IS NULL) AND (telefoon IS NULL) AND (email IS NULL)) OR ((telefoon IS NOT NULL) AND (email IS NOT NULL)))), 
    CONSTRAINT vrzkleden_email_check CHECK (((email)::text ~~ '%@%'::text)), 
    CONSTRAINT vrzkleden_email_check1 CHECK (((email)::text ~~ '%@%'::text)), 
    CONSTRAINT vrzkleden_pkey PRIMARY KEY (lidid) 
); 

CREATE TABLE vrzkverzekeringen ( 
    verzekeringsid numeric(10) DEFAULT nextval('seq_vrzkverzekeringen'::regclass) NOT NULL, 
    verantwoordelijkeid numeric(6) NOT NULL, 
    status numeric(2) NOT NULL, 
    factuurnr numeric(9) NULL, 
    facturatiedatum timestamp(6) NULL, 
    groepsnr varchar(6) NOT NULL, 
    groepsnaam varchar(50) NOT NULL, 
    groepsplaats varchar(50) NOT NULL, 
    datumvaninvulling timestamp(6) NOT NULL, 
    begindatum timestamp(6) NOT NULL, 
    einddatum timestamp(6) NOT NULL, 
    totkostprijs numeric(7, 2) NOT NULL, 
    opmerking varchar(500) NULL, 
    vvksmopmerking varchar(500) NULL, 
    afgedrukt varchar(1) DEFAULT 'N'::character varying NOT NULL, 
    afgewerkt varchar(1) DEFAULT 'N'::character varying NOT NULL, 
    lijstok varchar(1) DEFAULT 'N'::character varying NOT NULL, 
    typeid numeric(2) NOT NULL, 
    verzonden_ethias_datum timestamp(6) NULL, 
    goedkeuringsdatum timestamp(6) NULL, 
    betalingsdatum timestamp(6) NULL, 
    bijlage timestamp NULL, 
    CONSTRAINT "FACTUURNR" UNIQUE (factuurnr), 
    CONSTRAINT vrzkverzekeringen_afgedrukt_check CHECK (((afgedrukt)::text = ANY (ARRAY[('J'::character varying)::text, ('N'::character varying)::text]))), 
    CONSTRAINT vrzkverzekeringen_afgewerkt_check CHECK (((afgewerkt)::text = ANY (ARRAY[('J'::character varying)::text, ('N'::character varying)::text]))), 
    CONSTRAINT vrzkverzekeringen_begindatum_check CHECK ((to_date('20050101'::text, 'yyyymmdd'::text) <= begindatum)), 
    CONSTRAINT vrzkverzekeringen_check CHECK ((begindatum <= einddatum)), 
    CONSTRAINT vrzkverzekeringen_check1 CHECK (((((afgedrukt)::text = ANY (ARRAY[('J'::character varying)::text, ('N'::character varying)::text])) AND (factuurnr IS NOT NULL) AND (facturatiedatum IS NOT NULL)) OR (((afgedrukt)::text = 'N'::text) AND (factuurnr IS NULL) AND (facturatiedatum IS NULL)))), 
    CONSTRAINT vrzkverzekeringen_check2 CHECK ((((status = ANY (ARRAY[(10)::numeric, (20)::numeric, (40)::numeric])) AND ((afgedrukt)::text = 'N'::text) AND ((afgewerkt)::text = 'N'::text) AND ((lijstok)::text = 'N'::text)) OR ((status = (30)::numeric) AND (factuurnr IS NOT NULL)) OR (status = (99)::numeric))), 
    CONSTRAINT vrzkverzekeringen_datumvaninvulling_check CHECK ((to_date('20050101'::text, 'yyyymmdd'::text) <= datumvaninvulling)), 
    CONSTRAINT vrzkverzekeringen_facturatiedatum_check CHECK ((to_date('20050101'::text, 'yyyymmdd'::text) <= facturatiedatum)), 
    CONSTRAINT vrzkverzekeringen_groepsnr_check CHECK (((groepsnr)::text ~ '^[ABLOWX][0-9]{4}[DGKMPS]$'::text)), 
    CONSTRAINT vrzkverzekeringen_lijstok_check CHECK (((lijstok)::text = ANY (ARRAY[('J'::character varying)::text, ('N'::character varying)::text]))), 
    CONSTRAINT vrzkverzekeringen_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzkverzekeringen_status_check CHECK ((status = ANY (ARRAY[(10)::numeric, (20)::numeric, (30)::numeric, (40)::numeric, (99)::numeric]))), 
    CONSTRAINT vrzkverzekeringen_totkostprijs_check CHECK (((0)::numeric <= totkostprijs)), 
    CONSTRAINT vrzkverzekeringen_typeid_fkey FOREIGN KEY (typeid) REFERENCES vrzkverzekeringstypes(verzekeringstypeid), 
    CONSTRAINT vrzkverzekeringen_verantwoordelijkeid_fkey FOREIGN KEY (verantwoordelijkeid) REFERENCES vrzkleden(lidid) 
); 


CREATE TABLE vrzktypeethiasassistance (
    bestemmingsland varchar(60) NOT NULL,
    autotype varchar(30) NULL,
    automerk varchar(15) NULL,
    autokenteken varchar(10) NULL,
    autobouwjaar numeric(4) NULL,
    aanhangwagen numeric(1) NULL,
    verzekeringsid numeric(10) NOT NULL,
    inuits_vehicle_id uuid NULL,
    autochassis varchar(20) NULL,
    CONSTRAINT vrzktypeethiasassistance_aanhangwagen_check CHECK (((aanhangwagen IS NULL) OR (aanhangwagen = ANY (ARRAY[(0)::numeric, (1)::numeric])))),
    CONSTRAINT vrzktypeethiasassistance_autobouwjaar_check CHECK (((autobouwjaar IS NULL) OR ((1900)::numeric < autobouwjaar))),
    CONSTRAINT vrzktypeethiasassistance_check CHECK ((((autotype IS NULL) AND (automerk IS NULL) AND (autobouwjaar IS NULL) AND (aanhangwagen IS NULL)) OR ((autotype IS NOT NULL) AND (automerk IS NOT NULL) AND (autobouwjaar IS NOT NULL) AND (aanhangwagen IS NOT NULL)))),
    CONSTRAINT vrzktypeethiasassistance_pkey PRIMARY KEY (verzekeringsid),
    CONSTRAINT vrzktypeethiasassistance_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES vrzkverzekeringen(verzekeringsid)
);

CREATE INDEX "IDX_VRZKASSISTANCE_AUTOKENTEKE" ON public.vrzktypeethiasassistance USING btree (autokenteken);

CREATE TABLE vrzktypeevenement ( 
    ardactiviteit varchar(500) NOT NULL, 
    aantbezoekers numeric(2) NOT NULL, 
    postcode numeric(4) NOT NULL, 
    gemeente varchar(40) NOT NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    CONSTRAINT vrzktypeevenement_aantbezoekers_check CHECK ((aantbezoekers = ANY (ARRAY[(1)::numeric, (2)::numeric, (3)::numeric, (4)::numeric, (5)::numeric]))), 
    CONSTRAINT vrzktypeevenement_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzktypeevenement_postcode_check CHECK (((1000)::numeric <= postcode)), 
    CONSTRAINT vrzktypeevenement_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES vrzkverzekeringen(verzekeringsid) 
); 

CREATE TABLE vrzktypemateriaal ( 
    aardactiviteit varchar(500) NOT NULL, 
    postcode numeric(4) NULL, 
    gemeente varchar(40) NULL, 
    land varchar(60) DEFAULT NULL::character varying NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    CONSTRAINT vrzktypemateriaal_check CHECK ((((postcode IS NULL) AND (gemeente IS NULL) AND (land IS NOT NULL)) OR ((postcode IS NOT NULL) AND (gemeente IS NOT NULL) AND (land IS NULL)))), 
    CONSTRAINT vrzktypemateriaal_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzktypemateriaal_postcode_check CHECK (((postcode IS NULL) OR ((1000)::numeric <= postcode))), 
    CONSTRAINT vrzktypemateriaal_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES vrzkverzekeringen(verzekeringsid) 
); 

CREATE TABLE vrzktypetijdact ( 
    aardactiviteit varchar(500) NOT NULL, 
    postcode numeric(4) NULL, 
    gemeente varchar(40) NULL, 
    land varchar(60) NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    CONSTRAINT vrzktypetijdact_check CHECK ((((postcode IS NULL) AND (gemeente IS NULL) AND (land IS NOT NULL)) OR ((postcode IS NOT NULL) AND (gemeente IS NOT NULL) AND (land IS NULL)))), 
    CONSTRAINT vrzktypetijdact_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzktypetijdact_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES vrzkverzekeringen(verzekeringsid) 
); 

CREATE TABLE vrzktypetijdauto ( 
    keuze numeric(2) NOT NULL, 
    maxdekking varchar(1) NULL, 
    autotype varchar(30) DEFAULT 'PERSONENWAGEN'::character varying NOT NULL, 
    automerk varchar(15) NOT NULL, 
    autokenteken varchar(10) NOT NULL, 
    autobouwjaar numeric(4) NOT NULL, 
    autochassis varchar(20) NOT NULL, 
    aanhangwagen varchar(1) DEFAULT NULL::character varying NOT NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    inuits_vehicle_id uuid NULL, 
    CONSTRAINT vrzktypetijdauto_aanhangwagen_check CHECK (((aanhangwagen)::text = ANY (ARRAY[('0'::character varying)::text, ('1'::character varying)::text, ('2'::character varying)::text, ('3'::character varying)::text]))), 
    CONSTRAINT vrzktypetijdauto_autobouwjaar_check CHECK (((1900)::numeric < autobouwjaar)), 
    CONSTRAINT vrzktypetijdauto_autotype_check CHECK (((autotype)::text = ANY (ARRAY[('AUTO DUBBEL GEBRUIK'::character varying)::text, ('MINIBUS'::character varying)::text, ('PERSONENWAGEN'::character varying)::text, ('VRACHTWAGEN'::character varying)::text]))), 
    CONSTRAINT vrzktypetijdauto_check CHECK (((((keuze = (2)::numeric) OR (keuze = (23)::numeric)) AND (maxdekking IS NOT NULL)) OR ((keuze <> (2)::numeric) AND (keuze <> (23)::numeric) AND (maxdekking IS NULL)))), 
    CONSTRAINT vrzktypetijdauto_keuze_check CHECK ((keuze = ANY (ARRAY[(1)::numeric, (2)::numeric, (3)::numeric, (13)::numeric, (23)::numeric]))), 
    CONSTRAINT vrzktypetijdauto_maxdekking_check CHECK (((maxdekking IS NULL) OR ((maxdekking)::text = ANY (ARRAY[('A'::character varying)::text, ('B'::character varying)::text, ('C'::character varying)::text])))), 
    CONSTRAINT vrzktypetijdauto_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzktypetijdauto_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES vrzkverzekeringen(verzekeringsid) 
); 

CREATE INDEX "IDX_VRZKVERZEKERINGEN_BEGINDATUM" ON public.vrzkverzekeringen USING btree (begindatum); 
CREATE INDEX "IDX_VRZKVERZEKERINGEN_DATUMVAN" ON public.vrzkverzekeringen USING btree (datumvaninvulling); 
CREATE INDEX "IDX_VRZKVERZEKERINGEN_GROEPSNR" ON public.vrzkverzekeringen USING btree (groepsnr); 
CREATE INDEX "IDX_VRZKVERZEKERINGEN_STATUS" ON public.vrzkverzekeringen USING btree (status); 
CREATE INDEX "IDX_VRZKVERZEKERINGEN_TYPEID" ON public.vrzkverzekeringen USING btree (typeid); 
CREATE INDEX "IDX_VRZKVERZEKERINGEN_VERANTWOORDELIJKE" ON public.vrzkverzekeringen USING btree (verantwoordelijkeid); 
INSERT INTO vrzkverzekeringstypes (verzekeringstypeid,verzekeringstype,verzekeringstypeomschr,maxtermijn) VALUES 
 (2,'TypeTijdelijkeVerzekering','Tijdelijke verzekering niet-leden','31'), 
 (5,'TypeTijdelijkeAutoverzekering','Autoverzekering','30'), 
 (11,'BaVereniging','Burgerlijke aansprakelijkheid ondersteunende vereniging','366'), 
 (12,'ObaZaal','Objectieve aansprakelijkheid polyvalente zaal','366'), 
 (1,'TypeEenmaligeActiviteit','Verzekering voor een eenmalige activiteit','0'), 
 (3,'TypeEthiasAssistanceZonderAuto','Reisbijstand','0'), 
 (4,'TypeEthiasAssistanceMetAuto','Reisbijstand met de auto','0'), 
 (6,'TypeGroepsmateriaalVerzekering','Materiaalverzekering','30'), 
 (10,'TypeEvenementenVerzekering','Evenementenverzekering','0'); 
 
CREATE TABLE public.vrzknietleden ( 
    nietlidid numeric(6) DEFAULT nextval('seq_vrzknietleden'::regclass) NOT NULL, 
    naam varchar(255) NOT NULL, 
    voornaam varchar(255) NOT NULL, 
    telefoon varchar(15) NULL, 
    geboortedatum timestamp(6) NULL, 
    straat varchar(100) NULL, 
    nr varchar(5) DEFAULT NULL::character varying NULL, 
    bus varchar(5) DEFAULT NULL::character varying NULL, 
    postcode numeric(4) NULL, 
    gemeente varchar(100) NULL, 
    commentaar varchar(500) NULL, 
    inuits_id uuid NULL, 
    CONSTRAINT vrzknietleden_check CHECK ((((straat IS NULL) AND (nr IS NULL) AND (gemeente IS NULL) AND (postcode IS NULL)) OR ((straat IS NOT NULL) AND (nr IS NOT NULL) AND (gemeente IS NOT NULL) AND (postcode IS NOT NULL)))), 
    CONSTRAINT vrzknietleden_pkey PRIMARY KEY (nietlidid) 
); 

CREATE TABLE vrzkmateriaal ( 
    materiaalid numeric(6) DEFAULT nextval('seq_vrzkmateriaal'::regclass) NOT NULL, 
    eigenaaridnietlid numeric(6) NULL, 
    eigenaaridlid numeric(6) NULL, 
    aard varchar(50) NULL, 
    materieomschrijving varchar(500) NOT NULL, 
    aantal numeric(3) NOT NULL, 
    nieuwwaardeperstuk numeric(7, 2) NOT NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    inuits_id uuid NULL, 
    CONSTRAINT vrzkmateriaal_aantal_check CHECK ((((0)::numeric < aantal))), 
    CONSTRAINT vrzkmateriaal_check CHECK ((((eigenaaridnietlid IS NULL) OR (aard IS NOT NULL) OR ((eigenaaridnietlid IS NOT NULL) OR (aard IS NULL))))), 
    CONSTRAINT vrzkmateriaal_nieuwwaardeperstuk_check CHECK ((((0)::numeric < nieuwwaardeperstuk))), 
    CONSTRAINT vrzkmateriaal_pkey PRIMARY KEY (materiaalid) 
); 

CREATE TABLE vrzktypeeenact ( 
    aardactiviteit varchar(500) NOT NULL, 
    aantgroep numeric(2) NOT NULL, 
    postcode numeric(4) NOT NULL, 
    gemeente varchar(40) NOT NULL, 
    verzekeringsid numeric(10) NOT NULL, 
    CONSTRAINT vrzktypeeenact_aantgroep_check CHECK ((aantgroep = ANY (ARRAY[(1)::numeric, (2)::numeric, (3)::numeric, (4)::numeric, (5)::numeric, (6)::numeric, (7)::numeric, (8)::numeric, (9)::numeric]))), 
    CONSTRAINT vrzktypeeenact_pkey PRIMARY KEY (verzekeringsid), 
    CONSTRAINT vrzktypeeenact_verzekeringsid_fkey FOREIGN KEY (verzekeringsid) REFERENCES public.vrzkverzekeringen(verzekeringsid) 
); 