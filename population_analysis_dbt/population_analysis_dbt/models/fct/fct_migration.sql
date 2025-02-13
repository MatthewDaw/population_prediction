WITH inflow_migration AS (
    select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_inflow mi
    JOIN
    {{ ref('dim_state') }} ds on lower(mi.state_name) = lower(ds.state_name)
    where ds.id is not null
),
outflow_migration AS (
    select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_outflow mo
    JOIN
    {{ ref('dim_state') }} ds on lower(mo.state_name) = lower(ds.state_name)
    where ds.id is not null
)

select
    CAST(om.year AS NUMERIC) as year,
    om.state_id,
    om.state_name,
    CAST(om.number_of_individuals AS NUMERIC) as outflow_migration_number_of_individuals,
    CAST(im.number_of_individuals AS NUMERIC) as inflow_migration_number_of_individuals
from
    outflow_migration om
JOIN
    inflow_migration im
on
    om.year = im.year and om.state_id = im.state_id
WHERE
    om.state_id is not null and im.state_id is not null and om.year is not null and im.year is not null
