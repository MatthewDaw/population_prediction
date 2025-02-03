WITH pop_age_distribution_2010 AS (
        SELECT 2010 YEAR, * FROM {{ ref('ACSST1Y2010S0101_2025_02_02T173212') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2011 AS (
        SELECT 2011 YEAR, * FROM {{ ref('ACSST1Y2011S0101_2025_02_02T173202') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2012 AS (
        SELECT 2012 YEAR, * FROM {{ ref('ACSST1Y2012S0101_2025_02_02T173145') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2013 AS (
        SELECT 2013 YEAR, * FROM {{ ref('ACSST1Y2013S0101_2025_02_02T173135') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2014 AS (
        SELECT 2014 YEAR, * FROM {{ ref('ACSST1Y2014S0101_2025_02_02T173123') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2015 AS (
        SELECT 2015 YEAR, * FROM {{ ref('ACSST1Y2015S0101_2025_02_02T173013') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2016 AS (
        SELECT 2016 YEAR, * FROM {{ ref('ACSST1Y2016S0101_2025_02_02T173002') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2017 AS (
        SELECT 2017 YEAR, * FROM {{ ref('ACSST1Y2017S0101_2025_02_02T172954') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2018 AS (
        SELECT 2018 YEAR, * FROM {{ ref('ACSST1Y2018S0101_2025_02_02T172945') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2019 AS (
        SELECT 2019 YEAR, * FROM {{ ref('ACSST1Y2019S0101_2025_02_02T172933') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2021 AS (
        SELECT 2021 YEAR, * FROM {{ ref('ACSST1Y2021S0101_2025_02_02T172919') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2022 AS (
        SELECT 2022 YEAR, * FROM {{ ref('ACSST1Y2022S0101_2025_02_02T172905') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),
pop_age_distribution_2023 AS (
        SELECT 2023 YEAR, * FROM {{ ref('ACSST1Y2023S0101_2025_02_02T172858') }} where LABEL_GROUPING != 'AGE' LIMIT 19
    ),

early_eyars_joined as (
select * from pop_age_distribution_2010 
UNION ALL select * from pop_age_distribution_2011
UNION ALL select * from pop_age_distribution_2012
UNION ALL select * from pop_age_distribution_2013
UNION ALL select * from pop_age_distribution_2014
UNION ALL select * from pop_age_distribution_2015
UNION ALL select * from pop_age_distribution_2016
),

later_years_joined as (
select * from pop_age_distribution_2017
UNION ALL select * from pop_age_distribution_2018
UNION ALL select * from pop_age_distribution_2019
UNION ALL select * from pop_age_distribution_2021
UNION ALL select * from pop_age_distribution_2022
UNION ALL select * from pop_age_distribution_2023
),

early_years_renamed AS (
    SELECT 
        label_grouping AS label_grouping,
        year,
        CAST(alabamatotalestimate AS NUMERIC) AS alabama, 
        CAST(alaskatotalestimate AS NUMERIC) AS alaska, 
        CAST(arizonatotalestimate AS NUMERIC) AS arizona, 
        CAST(arkansastotalestimate AS NUMERIC) AS arkansas, 
        CAST(californiatotalestimate AS NUMERIC) AS california, 
        CAST(coloradototalestimate AS NUMERIC) AS colorado, 
        CAST(connecticuttotalestimate AS NUMERIC) AS connecticut, 
        CAST(delawaretotalestimate AS NUMERIC) AS delaware, 
        CAST(district_of_columbiatotalestimate AS NUMERIC) AS district_of_columbia, 
        CAST(floridatotalestimate AS NUMERIC) AS florida, 
        CAST(georgiatotalestimate AS NUMERIC) AS georgia, 
        CAST(hawaiitotalestimate AS NUMERIC) AS hawaii, 
        CAST(idahototalestimate AS NUMERIC) AS idaho, 
        CAST(illinoistotalestimate AS NUMERIC) AS illinois, 
        CAST(indianatotalestimate AS NUMERIC) AS indiana, 
        CAST(iowatotalestimate AS NUMERIC) AS iowa, 
        CAST(kansastotalestimate AS NUMERIC) AS kansas, 
        CAST(kentuckytotalestimate AS NUMERIC) AS kentucky, 
        CAST(louisianatotalestimate AS NUMERIC) AS louisiana, 
        CAST(mainetotalestimate AS NUMERIC) AS maine, 
        CAST(marylandtotalestimate AS NUMERIC) AS maryland, 
        CAST(massachusettstotalestimate AS NUMERIC) AS massachusetts, 
        CAST(michigantotalestimate AS NUMERIC) AS michigan, 
        CAST(minnesotatotalestimate AS NUMERIC) AS minnesota, 
        CAST(mississippitotalestimate AS NUMERIC) AS mississippi, 
        CAST(missouritotalestimate AS NUMERIC) AS missouri, 
        CAST(montanatotalestimate AS NUMERIC) AS montana, 
        CAST(nebraskatotalestimate AS NUMERIC) AS nebraska, 
        CAST(nevadatotalestimate AS NUMERIC) AS nevada, 
        CAST(new_hampshiretotalestimate AS NUMERIC) AS new_hampshire, 
        CAST(new_jerseytotalestimate AS NUMERIC) AS new_jersey, 
        CAST(new_mexicototalestimate AS NUMERIC) AS new_mexico, 
        CAST(new_yorktotalestimate AS NUMERIC) AS new_york, 
        CAST(north_carolinatotalestimate AS NUMERIC) AS north_carolina, 
        CAST(north_dakotatotalestimate AS NUMERIC) AS north_dakota, 
        CAST(ohiototalestimate AS NUMERIC) AS ohio, 
        CAST(oklahomatotalestimate AS NUMERIC) AS oklahoma, 
        CAST(oregontotalestimate AS NUMERIC) AS oregon, 
        CAST(pennsylvaniatotalestimate AS NUMERIC) AS pennsylvania, 
        CAST(rhode_islandtotalestimate AS NUMERIC) AS rhode_island, 
        CAST(south_carolinatotalestimate AS NUMERIC) AS south_carolina, 
        CAST(south_dakotatotalestimate AS NUMERIC) AS south_dakota, 
        CAST(tennesseetotalestimate AS NUMERIC) AS tennessee, 
        CAST(texastotalestimate AS NUMERIC) AS texas, 
        CAST(utahtotalestimate AS NUMERIC) AS utah, 
        CAST(vermonttotalestimate AS NUMERIC) AS vermont, 
        CAST(virginiatotalestimate AS NUMERIC) AS virginia, 
        CAST(washingtontotalestimate AS NUMERIC) AS washington, 
        CAST(west_virginiatotalestimate AS NUMERIC) AS west_virginia, 
        CAST(wisconsintotalestimate AS NUMERIC) AS wisconsin, 
        CAST(wyomingtotalestimate AS NUMERIC) AS wyoming, 
        CAST(puerto_ricototalestimate AS NUMERIC) AS puerto_rico
    FROM early_eyars_joined
),
later_years_renamed AS (
    SELECT 
        label_grouping AS label_grouping,
        year,
        CAST(alabamatotalestimate AS NUMERIC) AS alabama, 
        CAST(alaskatotalestimate AS NUMERIC) AS alaska, 
        CAST(arizonatotalestimate AS NUMERIC) AS arizona, 
        CAST(arkansastotalestimate AS NUMERIC) AS arkansas, 
        CAST(californiatotalestimate AS NUMERIC) AS california, 
        CAST(coloradototalestimate AS NUMERIC) AS colorado, 
        CAST(connecticuttotalestimate AS NUMERIC) AS connecticut, 
        CAST(delawaretotalestimate AS NUMERIC) AS delaware, 
        CAST(district_of_columbiatotalestimate AS NUMERIC) AS district_of_columbia, 
        CAST(floridatotalestimate AS NUMERIC) AS florida, 
        CAST(georgiatotalestimate AS NUMERIC) AS georgia, 
        CAST(hawaiitotalestimate AS NUMERIC) AS hawaii, 
        CAST(idahototalestimate AS NUMERIC) AS idaho, 
        CAST(illinoistotalestimate AS NUMERIC) AS illinois, 
        CAST(indianatotalestimate AS NUMERIC) AS indiana, 
        CAST(iowatotalestimate AS NUMERIC) AS iowa, 
        CAST(kansastotalestimate AS NUMERIC) AS kansas, 
        CAST(kentuckytotalestimate AS NUMERIC) AS kentucky, 
        CAST(louisianatotalestimate AS NUMERIC) AS louisiana, 
        CAST(mainetotalestimate AS NUMERIC) AS maine, 
        CAST(marylandtotalestimate AS NUMERIC) AS maryland, 
        CAST(massachusettstotalestimate AS NUMERIC) AS massachusetts, 
        CAST(michigantotalestimate AS NUMERIC) AS michigan, 
        CAST(minnesotatotalestimate AS NUMERIC) AS minnesota, 
        CAST(mississippitotalestimate AS NUMERIC) AS mississippi, 
        CAST(missouritotalestimate AS NUMERIC) AS missouri, 
        CAST(montanatotalestimate AS NUMERIC) AS montana, 
        CAST(nebraskatotalestimate AS NUMERIC) AS nebraska, 
        CAST(nevadatotalestimate AS NUMERIC) AS nevada, 
        CAST(new_hampshiretotalestimate AS NUMERIC) AS new_hampshire, 
        CAST(new_jerseytotalestimate AS NUMERIC) AS new_jersey, 
        CAST(new_mexicototalestimate AS NUMERIC) AS new_mexico, 
        CAST(new_yorktotalestimate AS NUMERIC) AS new_york, 
        CAST(north_carolinatotalestimate AS NUMERIC) AS north_carolina, 
        CAST(north_dakotatotalestimate AS NUMERIC) AS north_dakota, 
        CAST(ohiototalestimate AS NUMERIC) AS ohio, 
        CAST(oklahomatotalestimate AS NUMERIC) AS oklahoma, 
        CAST(oregontotalestimate AS NUMERIC) AS oregon, 
        CAST(pennsylvaniatotalestimate AS NUMERIC) AS pennsylvania, 
        CAST(rhode_islandtotalestimate AS NUMERIC) AS rhode_island, 
        CAST(south_carolinatotalestimate AS NUMERIC) AS south_carolina, 
        CAST(south_dakotatotalestimate AS NUMERIC) AS south_dakota, 
        CAST(tennesseetotalestimate AS NUMERIC) AS tennessee, 
        CAST(texastotalestimate AS NUMERIC) AS texas, 
        CAST(utahtotalestimate AS NUMERIC) AS utah, 
        CAST(vermonttotalestimate AS NUMERIC) AS vermont, 
        CAST(virginiatotalestimate AS NUMERIC) AS virginia, 
        CAST(washingtontotalestimate AS NUMERIC) AS washington, 
        CAST(west_virginiatotalestimate AS NUMERIC) AS west_virginia, 
        CAST(wisconsintotalestimate AS NUMERIC) AS wisconsin, 
        CAST(wyomingtotalestimate AS NUMERIC) AS wyoming, 
        CAST(puerto_ricototalestimate AS NUMERIC) AS puerto_rico
    FROM later_years_joined
)

select * from early_years_renamed
UNION ALL select * from later_years_renamed






