select
    gdp.state_id,
    gdp.state_name,
    gdp.year,
    gdp.gdp,
    births.births,
    house_unit_count.num_housing_units,
    housing_price_index.house_price_index,
    migration.outflow_migration_number_of_individuals,
    migration.inflow_migration_number_of_individuals,
    pop_age_distribution.percentage_under_5_years,
    pop_age_distribution.percentage_5_to_9_years,
    pop_age_distribution.percentage_10_to_14_years,
    pop_age_distribution.percentage_15_to_19_years,
    pop_age_distribution.percentage_20_to_24_years,
    pop_age_distribution.percentage_25_to_29_years,
    pop_age_distribution.percentage_30_to_34_years,
    pop_age_distribution.percentage_35_to_39_years,
    pop_age_distribution.percentage_40_to_44_years,
    pop_age_distribution.percentage_45_to_49_years,
    pop_age_distribution.percentage_50_to_54_years,
    pop_age_distribution.percentage_55_to_59_years,
    pop_age_distribution.percentage_60_to_64_years,
    pop_age_distribution.percentage_65_to_69_years,
    pop_age_distribution.percentage_70_to_74_years,
    pop_age_distribution.percentage_75_to_79_years,
    pop_age_distribution.percentage_80_to_84_years,
    pop_age_distribution.percentage_85_years_and_over
from
{{ ref('fct_gdp') }} as gdp
JOIN
{{ ref('fct_births') }} as births
ON
gdp.state_id = births.state_id and gdp.year = births.year
JOIN
{{ ref('fct_house_unit_count') }} house_unit_count
ON house_unit_count.state_id = births.state_id and house_unit_count.year = births.year
JOIN
{{ ref('fct_housing_price_index') }} as housing_price_index
ON housing_price_index.state_id = births.state_id and housing_price_index.year = births.year
JOIN
{{ ref('fct_migration') }} as migration
on migration.year = births.year and migration.state_id = births.state_id
JOIN
{{ ref('fct_population') }} as population
on population.state_id = births.state_id and population.year = births.year
JOIN
{{ ref('fct_pop_age_distribution') }} as pop_age_distribution
on pop_age_distribution.state_id = births.state_id and pop_age_distribution.year = births.year
