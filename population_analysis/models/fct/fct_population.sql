select
    ds.id as state_id,
    ds.state_name,
    sp.year,
    sp.population
from POP_PREDICTION.DEV.src_population sp
join POP_PREDICTION.DEV.dim_state ds
        ON sp.STATE = ds.state_abbreviation
