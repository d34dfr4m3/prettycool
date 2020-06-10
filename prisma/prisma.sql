SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.company_email (
    email text NOT NULL,
    id text NOT NULL,
    service_url text NOT NULL,
    target_id text NOT NULL
);

CREATE TABLE public.location (
    city text,
    continent text NOT NULL,
    country text NOT NULL,
    country_code text NOT NULL,
    id text NOT NULL,
    latitude numeric(65,30) NOT NULL,
    longitude numeric(65,30) NOT NULL,
    province text,
    timezone text NOT NULL
);


CREATE TABLE public.protocol (
    id text NOT NULL,
    port integer NOT NULL,
    service_name text NOT NULL
);


CREATE TABLE public.server (
    id text NOT NULL,
    ip text NOT NULL,
    ip_version text NOT NULL,
    location_id text NOT NULL
);

CREATE TABLE public.target (
    company_name text NOT NULL,
    domain text NOT NULL,
    id text NOT NULL
);
