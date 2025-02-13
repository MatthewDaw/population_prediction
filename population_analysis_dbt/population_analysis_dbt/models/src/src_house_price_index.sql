WITH seed_gdp_state AS (
    SELECT * FROM {{ ref('house_price_index_monthly_hist') }}
)
select * from seed_gdp_state
