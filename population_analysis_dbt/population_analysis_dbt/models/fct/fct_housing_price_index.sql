WITH unpivoted_house_price_index AS (
SELECT
    YEAR(MONTH) AS year,
    Region,
    House_Price_Index
FROM
    {{ ref('src_house_price_index') }}
UNPIVOT
(
    House_Price_Index FOR Region IN (
        EAST_NORTH_CENTRAL_NSA, EAST_NORTH_CENTRAL_SA, EAST_SOUTH_CENTRAL_NSA, EAST_SOUTH_CENTRAL_SA,
        MIDDLE_ATLANTIC_NSA, MIDDLE_ATLANTIC_SA, MOUNTAIN_NSA, MOUNTAIN_SA, NEW_ENGLAND_NSA, NEW_ENGLAND_SA,
        PACIFIC_NSA, PACIFIC_SA, SOUTH_ATLANTIC_NSA, SOUTH_ATLANTIC_SA, WEST_NORTH_CENTRAL_NSA, WEST_NORTH_CENTRAL_SA,
        WEST_SOUTH_CENTRAL_NSA, WEST_SOUTH_CENTRAL_SA, USA_NSA, USA_SA
    )
) AS unpivoted_data
ORDER BY MONTH, Region
)

select ds.id as state_id, ds.state_name, CAST(hpi.year AS NUMERIC) as year, CAST(hpi.house_price_index AS NUMERIC) as house_price_index from unpivoted_house_price_index as hpi
RIGHT JOIN
POP_PREDICTION.DEV.dim_state ds ON ds.region = hpi.region
