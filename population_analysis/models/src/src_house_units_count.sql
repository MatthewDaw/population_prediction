WITH housing_2010_to_2020 AS (
    SELECT
        GeographicArea,
        Census_Population,
        Year_2010,
        Year_2011,
        Year_2012,
        Year_2013,
        Year_2014,
        Year_2015,
        Year_2016,
        Year_2017,
        Year_2018,
        Year_2019 FROM {{ ref('housing_units2010_to2019') }}
),
housing_2020_to_2030 AS (
    SELECT
        Geographic_Area,
        Year_2020,
        Year_2021,
        Year_2022,
        Year_2023 FROM {{ ref('housing_units2020_to20230') }}
)


SELECT
    housing_2010_to_2020.GeographicArea AS GeographicArea,
    housing_2010_to_2020.Census_Population,
    housing_2010_to_2020.Year_2010,
    housing_2010_to_2020.Year_2011,
    housing_2010_to_2020.Year_2012,
    housing_2010_to_2020.Year_2013,
    housing_2010_to_2020.Year_2014,
    housing_2010_to_2020.Year_2015,
    housing_2010_to_2020.Year_2016,
    housing_2010_to_2020.Year_2017,
    housing_2010_to_2020.Year_2018,
    housing_2010_to_2020.Year_2019,
    housing_2020_to_2030.Year_2020,
    housing_2020_to_2030.Year_2021,
    housing_2020_to_2030.Year_2022,
    housing_2020_to_2030.Year_2023
FROM housing_2010_to_2020
LEFT JOIN housing_2020_to_2030
    ON housing_2010_to_2020.GeographicArea = housing_2020_to_2030.Geographic_Area
