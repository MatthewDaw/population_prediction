WITH state_in_flow_08_09 AS (
    SELECT 
        2008 as start_year,
        2009 as end_year,
        state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow0809
        group by state_name
    ),

state_in_flow_09_10 AS (
    SELECT
        2009 as start_year,
        2010 as end_year,
        state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow0910
        group by state_name
    ),

state_in_flow_10_11 AS (
    SELECT
        2010 as start_year,
        2011 as end_year,
        state_name,
        sum(Exmpt_Num) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1011
        group by state_name
    ),

state_in_flow_11_12 AS (
    SELECT
        2011 as start_year,
        2012 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1112
        group by y1_state_name
    ),

state_in_flow_12_13 AS (
    SELECT
        2012 as start_year,
        2013 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1213
        group by y1_state_name
    ),

state_in_flow_13_14 AS (
    SELECT
        2013 as start_year,
        2014 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1314
        group by y1_state_name
    ),

state_in_flow_14_15 AS (
    SELECT
        2014 as start_year,
        2015 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1415
        group by y1_state_name
    ),

state_in_flow_15_16 AS (
    SELECT
        2015 as start_year,
        2016 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1516
        group by y1_state_name
    ),

state_in_flow_16_17 AS (
    SELECT
        2016 as start_year,
        2017 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1617
        group by y1_state_name
    ),

state_in_flow_17_18 AS (
    SELECT
        2017 as start_year,
        2018 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1718
        group by y1_state_name
    ),

state_in_flow_18_19 AS (
    SELECT
        2018 as start_year,
        2019 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1819
        group by y1_state_name
    ),

state_in_flow_19_20 AS (
    SELECT
        2019 as start_year,
        2020 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow1920
        group by y1_state_name
    ),

state_in_flow_20_21 AS (
    SELECT
        2020 as start_year,
        2021 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow2021
        group by y1_state_name
    ),

state_in_flow_21_22 AS (
    SELECT
        2021 as start_year,
        2022 as end_year,
        y1_state_name,
        sum(n2) number_of_individuals
    FROM POP_PREDICTION.DEV.stateinflow2122
        group by y1_state_name
    )

SELECT * FROM state_in_flow_08_09
 UNION ALL 
SELECT * FROM state_in_flow_09_10
 UNION ALL 
SELECT * FROM state_in_flow_10_11
 UNION ALL 
SELECT * FROM state_in_flow_11_12
 UNION ALL 
SELECT * FROM state_in_flow_12_13
 UNION ALL 
SELECT * FROM state_in_flow_13_14
 UNION ALL 
SELECT * FROM state_in_flow_14_15
 UNION ALL 
SELECT * FROM state_in_flow_15_16
 UNION ALL 
SELECT * FROM state_in_flow_16_17
 UNION ALL 
SELECT * FROM state_in_flow_17_18
 UNION ALL 
SELECT * FROM state_in_flow_18_19
 UNION ALL 
SELECT * FROM state_in_flow_19_20
 UNION ALL 
SELECT * FROM state_in_flow_20_21
 UNION ALL 
SELECT * FROM state_in_flow_21_22
