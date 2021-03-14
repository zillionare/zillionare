-- version 0.6:
create table if not exists valuation
(
    id                     serial not null
        constraint valuation_pk
            primary key,
    code                   text   not null,
    pe                     real,
    turnover               real,
    pb                     real,
    ps                     real,
    pcf                    real,
    capital                numeric,
    market_cap             numeric,
    circulating_cap        numeric,
    circulating_market_cap numeric,
    pe_lyr                 real,
    frame                  date
);

alter table valuation
    owner to zillionare;

create unique index if not exists valuation_id_uindex
    on valuation (id);

create unique index if not exists valuation_code_frame_uindex
    on valuation (code, frame);
