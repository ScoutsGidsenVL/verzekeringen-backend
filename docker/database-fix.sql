CREATE SEQUENCE auth_group_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE auth_group_permissions_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE auth_permission_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE django_admin_log_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE django_content_type_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE django_migrations_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE scouts_auth_scoutsuser_groups_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE scouts_auth_scoutsuser_user_permissions_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE scouts_insurances_costvariable_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE scouts_insurances_country_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE scouts_insurances_country_insurance_types_id_seq MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzk_adres MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzk_bericht MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzk_vzw MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzkleden MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzkmateriaal MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzknietleden MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;
CREATE SEQUENCE seq_vrzkverzekeringen MINVALUE 0 NO MAXVALUE START 0 NO CYCLE;

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

-- Groups
INSERT INTO public.auth_group (name) VALUES 
('role_section_leader'), 
('role_group_leader'), 
('role_district_commissioner'), 
('role_administrator'), 
('role_super_admin');

-- Permissions
INSERT INTO public.auth_permission (name,content_type_id,codename) VALUES
('Can add log entry',1,'add_logentry'),
('Can change log entry',1,'change_logentry'),
('Can delete log entry',1,'delete_logentry'),
('Can view log entry',1,'view_logentry'),
('Can add permission',2,'add_permission'),
('Can change permission',2,'change_permission'),
('Can delete permission',2,'delete_permission'),
('Can view permission',2,'view_permission'),
('Can add group',3,'add_group'),
('Can change group',3,'change_group'),
('Can delete group',3,'delete_group'),
('Can view group',3,'view_group'),
('Can add content type',4,'add_contenttype'),
('Can change content type',4,'change_contenttype'),
('Can delete content type',4,'delete_contenttype'),
('Can view content type',4,'view_contenttype'),
('Can add session',5,'add_session'),
('Can change session',5,'change_session'),
('Can delete session',5,'delete_session'),
('Can view session',5,'view_session'),
('Can add inuits equipment',6,'add_inuitsequipment'),
('Can change inuits equipment',6,'change_inuitsequipment'),
('Can delete inuits equipment',6,'delete_inuitsequipment'),
('Can view inuits equipment',6,'view_inuitsequipment'),
('Can add inuits vehicle',7,'add_inuitsvehicle'),
('Can change inuits vehicle',7,'change_inuitsvehicle'),
('Can delete inuits vehicle',7,'delete_inuitsvehicle'),
('Can view inuits vehicle',7,'view_inuitsvehicle'),
('Can add inuits vehicle template',8,'add_inuitsvehicletemplate'),
('Can change inuits vehicle template',8,'change_inuitsvehicletemplate'),
('Can delete inuits vehicle template',8,'delete_inuitsvehicletemplate'),
('Can view inuits vehicle template',8,'view_inuitsvehicletemplate'),
('Can add inuits equipment template',9,'add_inuitsequipmenttemplate'),
('Can change inuits equipment template',9,'change_inuitsequipmenttemplate'),
('Can delete inuits equipment template',9,'delete_inuitsequipmenttemplate'),
('Can view inuits equipment template',9,'view_inuitsequipmenttemplate'),
('Can add activity insurance attachment',10,'add_activityinsuranceattachment'),
('Can change activity insurance attachment',10,'change_activityinsuranceattachment'),
('Can delete activity insurance attachment',10,'delete_activityinsuranceattachment'),
('Can view activity insurance attachment',10,'view_activityinsuranceattachment'),
('Can add event insurance attachment',11,'add_eventinsuranceattachment'),
('Can change event insurance attachment',11,'change_eventinsuranceattachment'),
('Can delete event insurance attachment',11,'delete_eventinsuranceattachment'),
('Can view event insurance attachment',11,'view_eventinsuranceattachment'),
('Can add insurance claim',12,'add_insuranceclaim'),
('Can change insurance claim',12,'change_insuranceclaim'),
('Can delete insurance claim',12,'delete_insuranceclaim'),
('Can view insurance claim',12,'view_insuranceclaim'),
('User can add a note to a claim',12,'add_insuranceclaim_note'),
('Administrative users can view a claim note',12,'view_insuranceclaim_note'),
('Users can add a claim case number',12,'add_insuranceclaim_case_number'),
('Administrative users can view a claim case number',12,'view_insuranceclaim_case_number'),
('User can view a list of claims',12,'list_insuranceclaims'),
('User can view the filename of a claim attachment',12,'view_insuranceclaimattachment_filename'),
('Can add insurance draft',13,'add_insurancedraft'),
('Can change insurance draft',13,'change_insurancedraft'),
('Can delete insurance draft',13,'delete_insurancedraft'),
('Can view insurance draft',13,'view_insurancedraft'),
('Can add insurance claim attachment',14,'add_insuranceclaimattachment'),
('Can change insurance claim attachment',14,'change_insuranceclaimattachment'),
('Can delete insurance claim attachment',14,'delete_insuranceclaimattachment'),
('Can view insurance claim attachment',14,'view_insuranceclaimattachment'),
('Can add inuits non member',15,'add_inuitsnonmember'),
('Can change inuits non member',15,'change_inuitsnonmember'),
('Can delete inuits non member',15,'delete_inuitsnonmember'),
('Can view inuits non member',15,'view_inuitsnonmember'),
('Can add inuits non member template',16,'add_inuitsnonmembertemplate'),
('Can change inuits non member template',16,'change_inuitsnonmembertemplate'),
('Can delete inuits non member template',16,'delete_inuitsnonmembertemplate'),
('Can view inuits non member template',16,'view_inuitsnonmembertemplate'),
('Can add inuits claim victim',17,'add_inuitsclaimvictim'),
('Can change inuits claim victim',17,'change_inuitsclaimvictim'),
('Can delete inuits claim victim',17,'delete_inuitsclaimvictim'),
('Can view inuits claim victim',17,'view_inuitsclaimvictim');

-- Group permissions
INSERT INTO public.auth_group_permissions (group_id,permission_id) VALUES 
(1,45), (1,46), (1,53), 
(2,45), (2,46), (2,53), 
(3,53), (3,49), (3,50), (3,51), (3,52), (3,54), 
(5,53);

CREATE TABLE vrzk_adres (
    adres_id numeric(38) DEFAULT nextval('seq_vrzk_adres'::regclass) NOT NULL,
    straat varchar(100) NOT NULL,
    nummer varchar(5) NOT NULL,
    bus varchar(5) NULL,
    postcode varchar(4) NOT NULL,
    gemeente varchar(40) NOT NULL,
    CONSTRAINT vrzk_adres_pkey PRIMARY KEY (adres_id)
);

CREATE TABLE vrzk_ba_vereniging (
    verzekeringsid numeric(38) NOT NULL,
    ba_type varchar(10) NOT NULL,
    vereniging_id numeric(38) NOT NULL,
    CONSTRAINT vrzk_ba_vereniging_pkey PRIMARY KEY (verzekeringsid)
);

CREATE TABLE vrzk_bericht (
    bericht_id numeric(10) DEFAULT nextval('seq_vrzk_bericht'::regclass) NOT NULL,
    verzekeringsid numeric(10) NOT NULL,
    type_bericht varchar(50) NOT NULL,
    ontvangers varchar(255) NOT NULL,
    verstuurd timestamp(0) DEFAULT now() NOT NULL,
    bericht varchar(4000) NULL,
    CONSTRAINT vrzk_bericht_pkey PRIMARY KEY (bericht_id)
);

CREATE TABLE vrzk_log (
    tijd timestamp(6) DEFAULT now() NOT NULL,
    message varchar(1500) NOT NULL
);

CREATE TABLE vrzk_oba_zaal (
    verzekeringsid numeric(38) NOT NULL,
    inrichting_aard varchar(25) NOT NULL,
    inrichting_adres_id numeric(38) NOT NULL,
    inrichting_opp numeric(4) NOT NULL,
    vereniging_id numeric(38) NULL,
    CONSTRAINT "UX_VZOBA_VERENIGING" UNIQUE (vereniging_id),
    CONSTRAINT vrzk_oba_zaal_pkey PRIMARY KEY (verzekeringsid)
);

CREATE TABLE vrzk_vereniging (
    vereniging_id numeric(38) DEFAULT nextval('seq_vrzk_vzw'::regclass) NOT NULL,
    naam varchar(255) NOT NULL,
    ondernemingsnr varchar(12) NULL,
    juridische_vorm varchar(21) NOT NULL,
    omschrijving varchar(255) NOT NULL,
    adres_id numeric(38) NOT NULL,
    contact_naam varchar(41) NOT NULL,
    contact_email varchar(255) NOT NULL,
    contact_tel varchar(20) NOT NULL,
    contact_fax varchar(20) NULL,
    contact_adres_id numeric(38) NOT NULL,
    CONSTRAINT vrzk_vereniging_check CHECK (
        (
            (juridische_vorm = 'VZW' AND ondernemingsnr ~ '^0[0-9]{3}-[0-9]{3}-[0-9]{3}$')
            OR
            (juridische_vorm = 'Feitelijke vereniging' AND ondernemingsnr IS NULL)
        )
    ),
    CONSTRAINT vrzk_vereniging_pkey PRIMARY KEY (vereniging_id)
);

CREATE TABLE vrzkassistpassagier (
    passagierid numeric(6) NOT NULL,
    verzekeringsid numeric(10) NOT NULL,
    CONSTRAINT vrzkassistpassagier_pkey PRIMARY KEY (passagierid)
);

CREATE TABLE vrzknietledentijd (
    nietledenid numeric(6) NOT NULL,
    verzekeringsid numeric(10) NOT NULL,
    CONSTRAINT vrzknietledentijd_pkey PRIMARY KEY (nietledenid)
);

CREATE TABLE vrzktijdautonietleden (
    bestuurderid numeric(6) NOT NULL,
    soort varchar(10) NOT NULL,
    verzekeringsid numeric(10) NOT NULL,
    CONSTRAINT vrzktijdautonietleden_pkey PRIMARY KEY (bestuurderid),
    CONSTRAINT vrzktijdautonietleden_soort_check CHECK (
        soort IN ('Eigenaar', 'Bestuurder')
    )
);
