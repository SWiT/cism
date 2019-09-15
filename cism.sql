-- Adminer 4.7.3 PostgreSQL dump

\connect "cism";

CREATE SEQUENCE user_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."cism_users" (
    "id" integer DEFAULT nextval('user_id_seq') NOT NULL,
    "username" character varying(20) NOT NULL,
    "password" character varying(32) NOT NULL
) WITH (oids = false);


CREATE SEQUENCE graph_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."graph" (
    "id" integer DEFAULT nextval('graph_id_seq') NOT NULL,
    "label" character varying(50),
    "inputdatatypeid" integer,
    "io" character varying(6),
    CONSTRAINT "graph_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE graph_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."graph_entries" (
    "id" integer DEFAULT nextval('graph_data_id_seq') NOT NULL,
    "graphid" integer,
    "ioid" integer,
    CONSTRAINT "graph_data_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE input_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."input" (
    "id" integer DEFAULT nextval('input_id_seq') NOT NULL,
    "inputtypeid" integer,
    "label" character varying(50),
    "color" character varying(7),
    "iodeviceid" integer,
    "pin" integer,
    CONSTRAINT "input_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE input_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."input_data" (
    "id" integer DEFAULT nextval('input_data_id_seq') NOT NULL,
    "inputid" integer,
    "datatypeid" integer,
    "data" double precision,
    "datetime" timestamp,
    "dataoffset" double precision,
    "dataraw" double precision,
    CONSTRAINT "input_data_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "input_data_datetime" ON "public"."input_data" USING btree ("datetime");


CREATE SEQUENCE input_data_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."input_data_type" (
    "id" integer DEFAULT nextval('input_data_type_id_seq') NOT NULL,
    "inputtypeid" integer,
    "label" character varying(50),
    "unit" character varying(50),
    "rangebegin" double precision,
    "rangeend" double precision,
    "accuracy" double precision,
    CONSTRAINT "input_data_type_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE input_data_offset_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."input_data_type_offset" (
    "id" integer DEFAULT nextval('input_data_offset_id_seq') NOT NULL,
    "inputid" integer,
    "inputdatatypeid" integer,
    "dataoffset" double precision DEFAULT '0'
) WITH (oids = false);


CREATE SEQUENCE input_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."input_type" (
    "id" integer DEFAULT nextval('input_type_id_seq') NOT NULL,
    "name" character varying(50),
    "maxsamplerate" integer,
    CONSTRAINT "input_type_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE io_device_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."io_device" (
    "id" integer DEFAULT nextval('io_device_id_seq') NOT NULL,
    "label" character varying(50),
    "port" character varying(255),
    "timeout" integer,
    "baud" integer,
    "samplerate" integer,
    CONSTRAINT "io_device_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE output_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."output" (
    "id" integer DEFAULT nextval('output_id_seq') NOT NULL,
    "outputtypeid" integer NOT NULL,
    "label" character varying(50),
    "color" character varying(7),
    "iodeviceid" integer,
    "defaultvalue" integer,
    "pin" integer,
    CONSTRAINT "output_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE output_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."output_data" (
    "id" integer DEFAULT nextval('output_data_id_seq') NOT NULL,
    "outputid" integer,
    "data" integer,
    "datetime" timestamp,
    CONSTRAINT "output_data_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "output_data_datetime" ON "public"."output_data" USING btree ("datetime");


CREATE SEQUENCE output_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."output_type" (
    "id" integer DEFAULT nextval('output_type_id_seq') NOT NULL,
    "name" character varying(50),
    "rangebegin" integer,
    "rangeend" integer,
    "maxupdaterate" integer,
    CONSTRAINT "output_type_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE output_data_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."output_value_labels" (
    "id" integer DEFAULT nextval('output_data_type_id_seq') NOT NULL,
    "outputtypeid" integer,
    "label" character varying(50),
    "value" integer,
    CONSTRAINT "output_data_type_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


CREATE SEQUENCE rule_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."rule" (
    "id" integer DEFAULT nextval('rule_id_seq') NOT NULL,
    "operation" character varying(2),
    "comparetype" character varying(10),
    "comparevalue" double precision,
    "compareinputid" integer,
    "outcomevalue" integer,
    "priority" integer,
    "sourcetype" character varying(6),
    "outcomeid" integer,
    "sourceinputid" integer,
    "sourceoutputid" integer,
    "compareoutputid" integer
) WITH (oids = false);


-- 2019-09-14 20:42:45.738401-04

