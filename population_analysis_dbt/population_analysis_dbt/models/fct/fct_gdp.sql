WITH unpivoted_gdp AS (
    SELECT
        RANKING_2023_HIGH_TO_LOW AS location_name,
        CAST(SPLIT_PART(year_column, '_', 2) AS INT) AS year,
        CAST(gdp_value AS NUMERIC) AS gdp
    FROM {{ ref('src_gdp_state') }}
    UNPIVOT (
        gdp_value FOR year_column IN (
            YEAR_1997, YEAR_1998, YEAR_1999, YEAR_2000, YEAR_2001, YEAR_2002, YEAR_2003,
            YEAR_2004, YEAR_2005, YEAR_2006, YEAR_2007, YEAR_2008, YEAR_2009, YEAR_2010,
            YEAR_2011, YEAR_2012, YEAR_2013, YEAR_2014, YEAR_2015, YEAR_2016, YEAR_2017,
            YEAR_2018, YEAR_2019, YEAR_2020, YEAR_2021, YEAR_2022, YEAR_2023
        )
    )
),
filtered_gdp AS (
    SELECT
        ds.ID AS state_id,
        ug.location_name as state_name,
        CAST(ug.year AS NUMERIC) as year,
        CAST(ug.gdp AS NUMERIC) as gdp
    FROM unpivoted_gdp ug
    JOIN {{ ref('dim_state') }} ds
        ON ug.location_name = ds.STATE_NAME
)
SELECT * FROM filtered_gdp

