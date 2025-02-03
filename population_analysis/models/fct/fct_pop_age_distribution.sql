with pop_age_distribution as (
select * from {{ ref('src_pop_age_distribution') }}  as pad
where pad.label_grouping != 'Total population'
),

Unpivoted AS (
    SELECT
        YEAR,
        REPLACE(REPLACE(REPLACE(LABEL_GROUPING, ' ', '_'), '-', '_to_'), '&', 'and') AS LABEL_GROUPING,
        REPLACE(STATE, '_', ' ') as STATE,
        Population
    FROM
        pop_age_distribution
    UNPIVOT (
        Population FOR STATE IN (
            ALABAMA, ALASKA, ARIZONA, ARKANSAS, CALIFORNIA, COLORADO, CONNECTICUT, DELAWARE,
            DISTRICT_OF_COLUMBIA, FLORIDA, GEORGIA, HAWAII, IDAHO, ILLINOIS, INDIANA, IOWA,
            KANSAS, KENTUCKY, LOUISIANA, MAINE, MARYLAND, MASSACHUSETTS, MICHIGAN, MINNESOTA,
            MISSISSIPPI, MISSOURI, MONTANA, NEBRASKA, NEVADA, NEW_HAMPSHIRE, NEW_JERSEY,
            NEW_MEXICO, NEW_YORK, NORTH_CAROLINA, NORTH_DAKOTA, OHIO, OKLAHOMA, OREGON,
            PENNSYLVANIA, RHODE_ISLAND, SOUTH_CAROLINA, SOUTH_DAKOTA, TENNESSEE, TEXAS,
            UTAH, VERMONT, VIRGINIA, WASHINGTON, WEST_VIRGINIA, WISCONSIN, WYOMING, PUERTO_RICO
        )
    ) AS unpvt
),
unpvt_with_state_id AS (
select ds.id as state_id, ds.state_name, up.year, up.label_grouping, up.population as population_percentage from Unpivoted up
join
    pop_prediction.dev.dim_state as ds
on lower(up.state) = lower(ds.state_name)
)


SELECT
    STATE_ID,
    STATE_NAME,
    YEAR,
    MAX(CASE WHEN LABEL_GROUPING = 'Under_5_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_under_5_years,
    MAX(CASE WHEN LABEL_GROUPING = '5_to_9_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_5_to_9_years,
    MAX(CASE WHEN LABEL_GROUPING = '10_to_14_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_10_to_14_years,
    MAX(CASE WHEN LABEL_GROUPING = '15_to_19_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_15_to_19_years,
    MAX(CASE WHEN LABEL_GROUPING = '20_to_24_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_20_to_24_years,
    MAX(CASE WHEN LABEL_GROUPING = '25_to_29_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_25_to_29_years,
    MAX(CASE WHEN LABEL_GROUPING = '30_to_34_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_30_to_34_years,
    MAX(CASE WHEN LABEL_GROUPING = '35_to_39_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_35_to_39_years,
    MAX(CASE WHEN LABEL_GROUPING = '40_to_44_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_40_to_44_years,
    MAX(CASE WHEN LABEL_GROUPING = '45_to_49_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_45_to_49_years,
    MAX(CASE WHEN LABEL_GROUPING = '50_to_54_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_50_to_54_years,
    MAX(CASE WHEN LABEL_GROUPING = '55_to_59_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_55_to_59_years,
    MAX(CASE WHEN LABEL_GROUPING = '60_to_64_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_60_to_64_years,
    MAX(CASE WHEN LABEL_GROUPING = '65_to_69_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_65_to_69_years,
    MAX(CASE WHEN LABEL_GROUPING = '70_to_74_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_70_to_74_years,
    MAX(CASE WHEN LABEL_GROUPING = '75_to_79_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_75_to_79_years,
    MAX(CASE WHEN LABEL_GROUPING = '80_to_84_years' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_80_to_84_years,
    MAX(CASE WHEN LABEL_GROUPING = '85_years_and_over' THEN POPULATION_PERCENTAGE ELSE NULL END) AS percentage_85_years_and_over
FROM
    unpvt_with_state_id
GROUP BY
    STATE_ID,
    STATE_NAME,
    YEAR
ORDER BY
    STATE_NAME,
    YEAR
