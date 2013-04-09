--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cism_users; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE cism_users (
    id integer NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(32) NOT NULL
);


ALTER TABLE public.cism_users OWNER TO swit;

--
-- Name: graph; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE graph (
    id integer NOT NULL,
    label character varying(50),
    inputdatatypeid integer,
    io character varying(6)
);


ALTER TABLE public.graph OWNER TO swit;

--
-- Name: graph_entries; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE graph_entries (
    id integer NOT NULL,
    graphid integer,
    ioid integer
);


ALTER TABLE public.graph_entries OWNER TO swit;

--
-- Name: graph_data_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE graph_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.graph_data_id_seq OWNER TO swit;

--
-- Name: graph_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE graph_data_id_seq OWNED BY graph_entries.id;


--
-- Name: graph_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE graph_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.graph_id_seq OWNER TO swit;

--
-- Name: graph_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE graph_id_seq OWNED BY graph.id;


--
-- Name: input; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE input (
    id integer NOT NULL,
    inputtypeid integer,
    label character varying(50),
    color character varying(7),
    iodeviceid integer,
    pin integer
);


ALTER TABLE public.input OWNER TO swit;

--
-- Name: input_data; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE input_data (
    id integer NOT NULL,
    inputid integer,
    datatypeid integer,
    data double precision,
    datetime timestamp without time zone
);


ALTER TABLE public.input_data OWNER TO swit;

--
-- Name: input_data_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE input_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.input_data_id_seq OWNER TO swit;

--
-- Name: input_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE input_data_id_seq OWNED BY input_data.id;


--
-- Name: input_data_type; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE input_data_type (
    id integer NOT NULL,
    inputtypeid integer,
    label character varying(50),
    unit character varying(50),
    rangebegin double precision,
    rangeend double precision,
    accuracy double precision
);


ALTER TABLE public.input_data_type OWNER TO swit;

--
-- Name: input_data_type_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE input_data_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.input_data_type_id_seq OWNER TO swit;

--
-- Name: input_data_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE input_data_type_id_seq OWNED BY input_data_type.id;


--
-- Name: input_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE input_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.input_id_seq OWNER TO swit;

--
-- Name: input_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE input_id_seq OWNED BY input.id;


--
-- Name: input_type; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE input_type (
    id integer NOT NULL,
    name character varying(50),
    maxsamplerate integer
);


ALTER TABLE public.input_type OWNER TO swit;

--
-- Name: input_type_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE input_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.input_type_id_seq OWNER TO swit;

--
-- Name: input_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE input_type_id_seq OWNED BY input_type.id;


--
-- Name: io_device; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE io_device (
    id integer NOT NULL,
    label character varying(50),
    port character varying(255),
    timeout integer,
    baud integer,
    samplerate integer
);


ALTER TABLE public.io_device OWNER TO swit;

--
-- Name: io_device_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE io_device_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.io_device_id_seq OWNER TO swit;

--
-- Name: io_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE io_device_id_seq OWNED BY io_device.id;


--
-- Name: output; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE output (
    id integer NOT NULL,
    outputtypeid integer NOT NULL,
    label character varying(50),
    color character varying(7),
    iodeviceid integer,
    defaultvalue integer,
    pin integer
);


ALTER TABLE public.output OWNER TO swit;

--
-- Name: output_data; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE output_data (
    id integer NOT NULL,
    outputid integer,
    data integer,
    datetime timestamp without time zone
);


ALTER TABLE public.output_data OWNER TO swit;

--
-- Name: output_data_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE output_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.output_data_id_seq OWNER TO swit;

--
-- Name: output_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE output_data_id_seq OWNED BY output_data.id;


--
-- Name: output_value_labels; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE output_value_labels (
    id integer NOT NULL,
    outputtypeid integer,
    label character varying(50),
    value integer
);


ALTER TABLE public.output_value_labels OWNER TO swit;

--
-- Name: output_data_type_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE output_data_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.output_data_type_id_seq OWNER TO swit;

--
-- Name: output_data_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE output_data_type_id_seq OWNED BY output_value_labels.id;


--
-- Name: output_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE output_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.output_id_seq OWNER TO swit;

--
-- Name: output_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE output_id_seq OWNED BY output.id;


--
-- Name: output_type; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE output_type (
    id integer NOT NULL,
    name character varying(50),
    rangebegin integer,
    rangeend integer,
    maxupdaterate integer
);


ALTER TABLE public.output_type OWNER TO swit;

--
-- Name: output_type_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE output_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.output_type_id_seq OWNER TO swit;

--
-- Name: output_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE output_type_id_seq OWNED BY output_type.id;


--
-- Name: rule; Type: TABLE; Schema: public; Owner: swit; Tablespace: 
--

CREATE TABLE rule (
    id integer NOT NULL,
    operation character varying(2),
    comparetype character varying(10),
    comparevalue double precision,
    compareinputid integer,
    outcomevalue integer,
    priority integer,
    sourcetype character varying(6),
    outcomeid integer,
    sourceinputid integer,
    sourceoutputid integer,
    compareoutputid integer
);


ALTER TABLE public.rule OWNER TO swit;

--
-- Name: rule_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE rule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rule_id_seq OWNER TO swit;

--
-- Name: rule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE rule_id_seq OWNED BY rule.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: swit
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO swit;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: swit
--

ALTER SEQUENCE user_id_seq OWNED BY cism_users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY cism_users ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY graph ALTER COLUMN id SET DEFAULT nextval('graph_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY graph_entries ALTER COLUMN id SET DEFAULT nextval('graph_data_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY input ALTER COLUMN id SET DEFAULT nextval('input_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY input_data ALTER COLUMN id SET DEFAULT nextval('input_data_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY input_data_type ALTER COLUMN id SET DEFAULT nextval('input_data_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY input_type ALTER COLUMN id SET DEFAULT nextval('input_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY io_device ALTER COLUMN id SET DEFAULT nextval('io_device_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY output ALTER COLUMN id SET DEFAULT nextval('output_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY output_data ALTER COLUMN id SET DEFAULT nextval('output_data_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY output_type ALTER COLUMN id SET DEFAULT nextval('output_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY output_value_labels ALTER COLUMN id SET DEFAULT nextval('output_data_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: swit
--

ALTER TABLE ONLY rule ALTER COLUMN id SET DEFAULT nextval('rule_id_seq'::regclass);


--
-- Name: graph_data_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY graph_entries
    ADD CONSTRAINT graph_data_pkey PRIMARY KEY (id);


--
-- Name: graph_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY graph
    ADD CONSTRAINT graph_pkey PRIMARY KEY (id);


--
-- Name: input_data_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY input_data
    ADD CONSTRAINT input_data_pkey PRIMARY KEY (id);


--
-- Name: input_data_type_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY input_data_type
    ADD CONSTRAINT input_data_type_pkey PRIMARY KEY (id);


--
-- Name: input_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY input
    ADD CONSTRAINT input_pkey PRIMARY KEY (id);


--
-- Name: input_type_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY input_type
    ADD CONSTRAINT input_type_pkey PRIMARY KEY (id);


--
-- Name: io_device_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY io_device
    ADD CONSTRAINT io_device_pkey PRIMARY KEY (id);


--
-- Name: output_data_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY output_data
    ADD CONSTRAINT output_data_pkey PRIMARY KEY (id);


--
-- Name: output_data_type_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY output_value_labels
    ADD CONSTRAINT output_data_type_pkey PRIMARY KEY (id);


--
-- Name: output_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY output
    ADD CONSTRAINT output_pkey PRIMARY KEY (id);


--
-- Name: output_type_pkey; Type: CONSTRAINT; Schema: public; Owner: swit; Tablespace: 
--

ALTER TABLE ONLY output_type
    ADD CONSTRAINT output_type_pkey PRIMARY KEY (id);


--
-- Name: input_data_datetime; Type: INDEX; Schema: public; Owner: swit; Tablespace: 
--

CREATE INDEX input_data_datetime ON input_data USING btree (datetime);


--
-- Name: output_data_datetime; Type: INDEX; Schema: public; Owner: swit; Tablespace: 
--

CREATE INDEX output_data_datetime ON output_data USING btree (datetime);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

