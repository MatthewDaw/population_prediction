WITH seed_gdp_state AS (
    SELECT * FROM {{ ref('GDP_All_States') }}
)

select * from seed_gdp_state
