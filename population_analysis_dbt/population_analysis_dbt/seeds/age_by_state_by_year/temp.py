man = """WITH inflow_migration AS (
    select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_inflow mi
    JOIN
    {{ ref('dim_state') }} ds on mi.state_name = ds.state_name
    where ds.id is not null
),
outflow_migration AS (
    select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_outflow mo
    JOIN
    {{ ref('dim_state') }} ds on mo.state_name = ds.state_name
    where ds.id is not null
)

select
    om.year,
    om.state_id,
    om.state_name,
    om.number_of_individuals as outflow_migration_number_of_individuals,
    im.number_of_individuals as inflow_migration_number_of_individuals
from
    outflow_migration om
JOIN
    inflow_migration im
on
    om.year = im.year and om.state_id = im.state_id
WHERE
    om.state_id is not null and im.state_id is not null and om.year is not null and im.year is not null

"""
if __name__ == "__main__":
    cow = man.split("{{ ref('")
    rill = "POP_PREDICTION.DEV.".join(cow)
    out = "".join(rill.split("') }}"))
    print(out)

# # fct_births.sql                  fct_house_unit_count.sql        fct_marriage_status.sql         fct_pop_age_distribution.sql
# # fct_gdp.sql                     fct_housing_price_index.sql     fct_migration.sql               fct_population.sql
#
if __name__ == "__main__":
    table_names = [
        "fct_births",
        "fct_house_unit_count",
        "fct_marriage_status",
        "fct_pop_age_distribution",
        "fct_gdp",
        "fct_housing_price_index",
        "fct_migration",
        "fct_population",
    ]

    query = ""
    for table_name in table_names:
        query += f"select count(*), year, '{table_name}' as table_name from POP_PREDICTION.DEV.{table_name} group by year \nUNION ALL \n"

    print(query)
#
