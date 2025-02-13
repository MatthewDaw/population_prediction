WITH grouped_housing_price_index AS (
    SELECT state_id, year, AVG(house_price_index) AS house_price_index
    FROM {{ ref('fct_housing_price_index') }}
    GROUP BY state_id, year
)

SELECT
    AVG(population.population) AS avg_population,
    gdp.year,
    AVG(gdp.gdp) AS avg_gdp,
    AVG(births.births) AS avg_births,
    AVG(house_unit_count.num_housing_units) AS avg_housing_units,
    AVG(grouped_housing_price_index.house_price_index) AS avg_house_price_index,
    AVG(migration.outflow_migration_number_of_individuals) AS avg_outflow_migration,
    AVG(migration.inflow_migration_number_of_individuals) AS avg_inflow_migration,
    AVG(pop_age_distribution.percentage_under_5_years) AS avg_percentage_under_5_years,
    AVG(pop_age_distribution.percentage_5_to_9_years) AS avg_percentage_5_to_9_years,
    AVG(pop_age_distribution.percentage_10_to_14_years) AS avg_percentage_10_to_14_years,
    AVG(pop_age_distribution.percentage_15_to_19_years) AS avg_percentage_15_to_19_years,
    AVG(pop_age_distribution.percentage_20_to_24_years) AS avg_percentage_20_to_24_years,
    AVG(pop_age_distribution.percentage_25_to_29_years) AS avg_percentage_25_to_29_years,
    AVG(pop_age_distribution.percentage_30_to_34_years) AS avg_percentage_30_to_34_years,
    AVG(pop_age_distribution.percentage_35_to_39_years) AS avg_percentage_35_to_39_years,
    AVG(pop_age_distribution.percentage_40_to_44_years) AS avg_percentage_40_to_44_years,
    AVG(pop_age_distribution.percentage_45_to_49_years) AS avg_percentage_45_to_49_years,
    AVG(pop_age_distribution.percentage_50_to_54_years) AS avg_percentage_50_to_54_years,
    AVG(pop_age_distribution.percentage_55_to_59_years) AS avg_percentage_55_to_59_years,
    AVG(pop_age_distribution.percentage_60_to_64_years) AS avg_percentage_60_to_64_years,
    AVG(pop_age_distribution.percentage_65_to_69_years) AS avg_percentage_65_to_69_years,
    AVG(pop_age_distribution.percentage_70_to_74_years) AS avg_percentage_70_to_74_years,
    AVG(pop_age_distribution.percentage_75_to_79_years) AS avg_percentage_75_to_79_years,
    AVG(pop_age_distribution.percentage_80_to_84_years) AS avg_percentage_80_to_84_years,
    AVG(pop_age_distribution.percentage_85_years_and_over) AS avg_percentage_85_years_and_over
FROM {{ ref('fct_gdp') }} AS gdp
JOIN {{ ref('fct_births') }} AS births
    ON gdp.state_id = births.state_id
    AND gdp.year = births.year
JOIN {{ ref('fct_house_unit_count') }} AS house_unit_count
    ON house_unit_count.state_id = births.state_id
    AND house_unit_count.year = births.year
JOIN grouped_housing_price_index
    ON grouped_housing_price_index.state_id = births.state_id
    AND grouped_housing_price_index.year = births.year
JOIN {{ ref('fct_migration') }} AS migration
    ON migration.year = births.year
    AND migration.state_id = births.state_id
JOIN {{ ref('fct_population') }} AS population
    ON population.state_id = births.state_id
    AND population.year = births.year
JOIN {{ ref('fct_pop_age_distribution') }} AS pop_age_distribution
    ON pop_age_distribution.state_id = births.state_id
    AND pop_age_distribution.year = births.year
GROUP BY gdp.year