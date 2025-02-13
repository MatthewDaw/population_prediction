with housing_units as (
SELECT
    LTRIM(REPLACE(GEOGRAPHICAREA, '.', '')) AS GEOGRAPHICAREA,
    CAST(SUBSTRING(Year, 6, 4) AS INT) AS Year,
    num_housing_units
FROM
    {{ ref('src_house_units_count') }}
UNPIVOT
(
    num_housing_units FOR Year IN (
        YEAR_2010, YEAR_2011, YEAR_2012, YEAR_2013, YEAR_2014,
        YEAR_2015, YEAR_2016, YEAR_2017, YEAR_2018, YEAR_2019,
        YEAR_2020, YEAR_2021, YEAR_2022, YEAR_2023
    )
) AS unpivoted_data
ORDER BY GEOGRAPHICAREA, Year
)

select ds.id as state_id, CAST(hu.year AS NUMERIC) as year, ds.state_name, CAST(hu.num_housing_units AS NUMERIC) as num_housing_units from 
housing_units hu
JOIN 
{{ ref('dim_state') }} ds on lower(ds.state_name) = lower(hu.GEOGRAPHICAREA)
