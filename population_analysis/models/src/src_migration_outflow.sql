WITH state_out_flow_08_09 AS (
    SELECT
        2008 as start_year,
        2009 as end_year,
        state_name as state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM {{ ref('stateoutflow0809') }}
        group by state_name
    ),

state_out_flow_09_10 AS (
    SELECT
        2009 as start_year,
        2010 as end_year,
        state_name as state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM {{ ref('stateoutflow0910') }}
        group by state_name
    ),

state_out_flow_10_11 AS (
    SELECT
        2010 as start_year,
        2011 as end_year,
        state_name as state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM {{ ref('stateoutflow1011') }}
        group by state_name
    ),

state_out_flow_11_12 AS (
    SELECT
        2011 as start_year,
        2012 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1112') }}
        group by state_name
    ),

state_out_flow_12_13 AS (
    SELECT
        2012 as start_year,
        2013 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1213') }}
        group by state_name
    ),

state_out_flow_13_14 AS (
    SELECT
        2013 as start_year,
        2014 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1314') }}
        group by state_name
    ),

state_out_flow_14_15 AS (
    SELECT
        2014 as start_year,
        2015 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1415') }}
        group by state_name
    ),

state_out_flow_15_16 AS (
    SELECT
        2015 as start_year,
        2016 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1516') }}
        group by state_name
    ),

state_out_flow_16_17 AS (
    SELECT
        2016 as start_year,
        2017 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1617') }}
        group by state_name
    ),

state_out_flow_18_19 AS (
    SELECT
        2018 as start_year,
        2019 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1819') }}
        group by state_name
    ),

state_out_flow_19_20 AS (
    SELECT
        2019 as start_year,
        2020 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow1920') }}
        group by state_name
    ),

state_out_flow_20_21 AS (
    SELECT
        2020 as start_year,
        2021 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow2021') }}
        group by state_name
    ),

state_out_flow_21_22 AS (
    SELECT
        2021 as start_year,
        2022 as end_year,
        y2_state_name as state_name,
        sum(n2) number_of_individuals
    FROM {{ ref('stateoutflow2122') }}
        group by state_name
    )


SELECT * FROM state_out_flow_08_09
UNION ALL
SELECT * FROM state_out_flow_09_10
UNION ALL
SELECT * FROM state_out_flow_10_11
UNION ALL
SELECT * FROM state_out_flow_11_12
UNION ALL
SELECT * FROM state_out_flow_12_13
UNION ALL
SELECT * FROM state_out_flow_13_14
UNION ALL
SELECT * FROM state_out_flow_14_15
UNION ALL
SELECT * FROM state_out_flow_15_16
UNION ALL
SELECT * FROM state_out_flow_16_17
UNION ALL
SELECT * FROM state_out_flow_18_19
UNION ALL
SELECT * FROM state_out_flow_19_20
UNION ALL
SELECT * FROM state_out_flow_20_21
UNION ALL
SELECT * FROM state_out_flow_21_22
