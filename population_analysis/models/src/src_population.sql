WITH population AS (
    SELECT * FROM {{ ref('historical_state_population_by_year') }}
)

select * from population

