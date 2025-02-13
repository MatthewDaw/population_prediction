select
    ds.id as state_id,
    ds.state_name,
    CAST(sp.year AS NUMERIC) as year,
    CAST(sp.population AS NUMERIC) as population
from {{ ref('src_population') }} sp
join POP_PREDICTION.DEV.dim_state ds
        ON sp.STATE = ds.state_abbreviation

