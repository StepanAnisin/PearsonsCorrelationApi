-- Database: usersstatistics

-- DROP DATABASE usersstatistics;

CREATE DATABASE usersstatistics
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

GRANT ALL ON DATABASE usersstatistics TO postgres;

GRANT TEMPORARY, CONNECT ON DATABASE usersstatistics TO PUBLIC;

\c usersstatistics
-- Table: public.pearsonscorrelation

-- DROP TABLE public.pearsonscorrelation;

CREATE TABLE IF NOT EXISTS public.pearsonscorrelation
(
    user_id integer NOT NULL,
    x_data_type character varying(50) COLLATE pg_catalog."default",
    y_data_type character varying(50) COLLATE pg_catalog."default",
    value double precision,
    p_value double precision,
    CONSTRAINT "PearsonsCorrelation_pkey" PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE public.pearsonscorrelation
    OWNER to postgres;
