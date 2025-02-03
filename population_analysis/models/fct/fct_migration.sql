WITH inflow_migration AS (
select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_inflow mi
JOIN
pop_prediction.dev.dim_state ds on mi.state_name = ds.state_name
where ds.id is not null
),
outflow_migration AS (
select start_year as year, ds.id as state_id, ds.state_name, number_of_individuals from pop_prediction.dev.src_migration_outflow mo
JOIN
pop_prediction.dev.dim_state ds on mo.state_name = ds.state_name
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

