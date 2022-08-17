SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', FALSE);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS postgis_raster WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS postgis_sfcgal WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS address_standardizer WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS address_standardizer_data_us WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

SET default_tablespace = '';
SET default_table_access_method = heap;

CREATE TABLE public.thing
    (
        uuid uuid DEFAULT public.uuid_generate_v4() NOT NULL
    );
ALTER TABLE public.thing OWNER TO postgres;
ALTER TABLE ONLY public.thing ADD CONSTRAINT thing_pkey PRIMARY KEY (uuid);

CREATE TABLE public.thing_location_stat
    (
        "timestamp" timestamp WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'::text) NOT NULL,
        location    public.geometry                                                   NOT NULL,
        thing_uuid  uuid                                                              NOT NULL
    );
ALTER TABLE public.thing_location_stat OWNER TO postgres;
ALTER TABLE ONLY public.thing_location_stat ADD CONSTRAINT thing_uuid_thing_uuid FOREIGN KEY (thing_uuid) REFERENCES public.thing (uuid) DEFERRABLE INITIALLY DEFERRED;

INSERT INTO public.thing DEFAULT
VALUES;

INSERT INTO public.thing_location_stat
    (
        location,
        thing_uuid
    )
VALUES
    (
        public.ST_SetSRID(public.ST_MakePoint(115.8613, -31.9523), 4236),
        (
            SELECT uuid
            FROM public.thing
            LIMIT 1
        )
    );
