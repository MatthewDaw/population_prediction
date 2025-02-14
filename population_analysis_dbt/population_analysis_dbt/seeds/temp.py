cow = """WITH pop_age_distribution_2010 AS (
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
    WHERE label_grouping != 'Total population'
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
),

-- select * from later_years_renamed

normalized_years AS (
    SELECT
        main.label_grouping,
        main.year,
        main.ALABAMA / total_population.ALABAMA AS ALABAMA,
        main.ALASKA / total_population.ALASKA AS ALASKA,
        main.ARIZONA / total_population.ARIZONA AS ARIZONA,
        main.ARKANSAS / total_population.ARKANSAS AS ARKANSAS,
        main.CALIFORNIA / total_population.CALIFORNIA AS CALIFORNIA,
        main.COLORADO / total_population.COLORADO AS COLORADO,
        main.CONNECTICUT / total_population.CONNECTICUT AS CONNECTICUT,
        main.DELAWARE / total_population.DELAWARE AS DELAWARE,
        main.DISTRICT_OF_COLUMBIA / total_population.DISTRICT_OF_COLUMBIA AS DISTRICT_OF_COLUMBIA,
        main.FLORIDA / total_population.FLORIDA AS FLORIDA,
        main.GEORGIA / total_population.GEORGIA AS GEORGIA,
        main.HAWAII / total_population.HAWAII AS HAWAII,
        main.IDAHO / total_population.IDAHO AS IDAHO,
        main.ILLINOIS / total_population.ILLINOIS AS ILLINOIS,
        main.INDIANA / total_population.INDIANA AS INDIANA,
        main.IOWA / total_population.IOWA AS IOWA,
        main.KANSAS / total_population.KANSAS AS KANSAS,
        main.KENTUCKY / total_population.KENTUCKY AS KENTUCKY,
        main.LOUISIANA / total_population.LOUISIANA AS LOUISIANA,
        main.MAINE / total_population.MAINE AS MAINE,
        main.MARYLAND / total_population.MARYLAND AS MARYLAND,
        main.MASSACHUSETTS / total_population.MASSACHUSETTS AS MASSACHUSETTS,
        main.MICHIGAN / total_population.MICHIGAN AS MICHIGAN,
        main.MINNESOTA / total_population.MINNESOTA AS MINNESOTA,
        main.MISSISSIPPI / total_population.MISSISSIPPI AS MISSISSIPPI,
        main.MISSOURI / total_population.MISSOURI AS MISSOURI,
        main.MONTANA / total_population.MONTANA AS MONTANA,
        main.NEBRASKA / total_population.NEBRASKA AS NEBRASKA,
        main.NEVADA / total_population.NEVADA AS NEVADA,
        main.NEW_HAMPSHIRE / total_population.NEW_HAMPSHIRE AS NEW_HAMPSHIRE,
        main.NEW_JERSEY / total_population.NEW_JERSEY AS NEW_JERSEY,
        main.NEW_MEXICO / total_population.NEW_MEXICO AS NEW_MEXICO,
        main.NEW_YORK / total_population.NEW_YORK AS NEW_YORK,
        main.NORTH_CAROLINA / total_population.NORTH_CAROLINA AS NORTH_CAROLINA,
        main.NORTH_DAKOTA / total_population.NORTH_DAKOTA AS NORTH_DAKOTA,
        main.OHIO / total_population.OHIO AS OHIO,
        main.OKLAHOMA / total_population.OKLAHOMA AS OKLAHOMA,
        main.OREGON / total_population.OREGON AS OREGON,
        main.PENNSYLVANIA / total_population.PENNSYLVANIA AS PENNSYLVANIA,
        main.RHODE_ISLAND / total_population.RHODE_ISLAND AS RHODE_ISLAND,
        main.SOUTH_CAROLINA / total_population.SOUTH_CAROLINA AS SOUTH_CAROLINA,
        main.SOUTH_DAKOTA / total_population.SOUTH_DAKOTA AS SOUTH_DAKOTA,
        main.TENNESSEE / total_population.TENNESSEE AS TENNESSEE,
        main.TEXAS / total_population.TEXAS AS TEXAS,
        main.UTAH / total_population.UTAH AS UTAH,
        main.VERMONT / total_population.VERMONT AS VERMONT,
        main.VIRGINIA / total_population.VIRGINIA AS VIRGINIA,
        main.WASHINGTON / total_population.WASHINGTON AS WASHINGTON,
        main.WEST_VIRGINIA / total_population.WEST_VIRGINIA AS WEST_VIRGINIA,
        main.WISCONSIN / total_population.WISCONSIN AS WISCONSIN,
        main.WYOMING / total_population.WYOMING AS WYOMING,
        main.PUERTO_RICO / total_population.PUERTO_RICO AS PUERTO_RICO
    FROM later_years_renamed main
    JOIN later_years_renamed total_population
        ON main.year = total_population.year
        AND total_population.label_grouping = 'Total population'
    WHERE main.label_grouping != 'Total population'
),


pop_for_2019 AS (
    SELECT * FROM normalized_years WHERE year = 2019
),
pop_for_2021 AS (
    SELECT * FROM normalized_years WHERE year = 2021
),
stats_for_2020 AS (
SELECT
    pop_for_2019.label_grouping,
    2020 as year,
    (pop_for_2019.alabama + pop_for_2021.alabama) / 2 AS alabama,
    (pop_for_2019.alaska + pop_for_2021.alaska) / 2 AS alaska,
    (pop_for_2019.arizona + pop_for_2021.arizona) / 2 AS arizona,
    (pop_for_2019.arkansas + pop_for_2021.arkansas) / 2 AS arkansas,
    (pop_for_2019.california + pop_for_2021.california) / 2 AS california,
    (pop_for_2019.colorado + pop_for_2021.colorado) / 2 AS colorado,
    (pop_for_2019.connecticut + pop_for_2021.connecticut) / 2 AS connecticut,
    (pop_for_2019.delaware + pop_for_2021.delaware) / 2 AS delaware,
    (pop_for_2019.district_of_columbia + pop_for_2021.district_of_columbia) / 2 AS district_of_columbia,
    (pop_for_2019.florida + pop_for_2021.florida) / 2 AS florida,
    (pop_for_2019.georgia + pop_for_2021.georgia) / 2 AS georgia,
    (pop_for_2019.hawaii + pop_for_2021.hawaii) / 2 AS hawaii,
    (pop_for_2019.idaho + pop_for_2021.idaho) / 2 AS idaho,
    (pop_for_2019.illinois + pop_for_2021.illinois) / 2 AS illinois,
    (pop_for_2019.indiana + pop_for_2021.indiana) / 2 AS indiana,
    (pop_for_2019.iowa + pop_for_2021.iowa) / 2 AS iowa,
    (pop_for_2019.kansas + pop_for_2021.kansas) / 2 AS kansas,
    (pop_for_2019.kentucky + pop_for_2021.kentucky) / 2 AS kentucky,
    (pop_for_2019.louisiana + pop_for_2021.louisiana) / 2 AS louisiana,
    (pop_for_2019.maine + pop_for_2021.maine) / 2 AS maine,
    (pop_for_2019.maryland + pop_for_2021.maryland) / 2 AS maryland,
    (pop_for_2019.massachusetts + pop_for_2021.massachusetts) / 2 AS massachusetts,
    (pop_for_2019.michigan + pop_for_2021.michigan) / 2 AS michigan,
    (pop_for_2019.minnesota + pop_for_2021.minnesota) / 2 AS minnesota,
    (pop_for_2019.mississippi + pop_for_2021.mississippi) / 2 AS mississippi,
    (pop_for_2019.missouri + pop_for_2021.missouri) / 2 AS missouri,
    (pop_for_2019.montana + pop_for_2021.montana) / 2 AS montana,
    (pop_for_2019.nebraska + pop_for_2021.nebraska) / 2 AS nebraska,
    (pop_for_2019.nevada + pop_for_2021.nevada) / 2 AS nevada,
    (pop_for_2019.new_hampshire + pop_for_2021.new_hampshire) / 2 AS new_hampshire,
    (pop_for_2019.new_jersey + pop_for_2021.new_jersey) / 2 AS new_jersey,
    (pop_for_2019.new_mexico + pop_for_2021.new_mexico) / 2 AS new_mexico,
    (pop_for_2019.new_york + pop_for_2021.new_york) / 2 AS new_york,
    (pop_for_2019.north_carolina + pop_for_2021.north_carolina) / 2 AS north_carolina,
    (pop_for_2019.north_dakota + pop_for_2021.north_dakota) / 2 AS north_dakota,
    (pop_for_2019.ohio + pop_for_2021.ohio) / 2 AS ohio,
    (pop_for_2019.oklahoma + pop_for_2021.oklahoma) / 2 AS oklahoma,
    (pop_for_2019.oregon + pop_for_2021.oregon) / 2 AS oregon,
    (pop_for_2019.pennsylvania + pop_for_2021.pennsylvania) / 2 AS pennsylvania,
    (pop_for_2019.rhode_island + pop_for_2021.rhode_island) / 2 AS rhode_island,
    (pop_for_2019.south_carolina + pop_for_2021.south_carolina) / 2 AS south_carolina,
    (pop_for_2019.south_dakota + pop_for_2021.south_dakota) / 2 AS south_dakota,
    (pop_for_2019.tennessee + pop_for_2021.tennessee) / 2 AS tennessee,
    (pop_for_2019.texas + pop_for_2021.texas) / 2 AS texas,
    (pop_for_2019.utah + pop_for_2021.utah) / 2 AS utah,
    (pop_for_2019.vermont + pop_for_2021.vermont) / 2 AS vermont,
    (pop_for_2019.virginia + pop_for_2021.virginia) / 2 AS virginia,
    (pop_for_2019.washington + pop_for_2021.washington) / 2 AS washington,
    (pop_for_2019.west_virginia + pop_for_2021.west_virginia) / 2 AS west_virginia,
    (pop_for_2019.wisconsin + pop_for_2021.wisconsin) / 2 AS wisconsin,
    (pop_for_2019.wyoming + pop_for_2021.wyoming) / 2 AS wyoming,
    (pop_for_2019.puerto_rico + pop_for_2021.puerto_rico) / 2 AS puerto_rico
FROM pop_for_2019
JOIN pop_for_2021
ON pop_for_2019.label_grouping = pop_for_2021.label_grouping
)
select * from early_years_renamed
UNION ALL select * from normalized_years
UNION ALL select * from stats_for_2020
"""

bill = ("POP_PREDICTION.DEV.".join(cow.split("{{ ref('"))).replace("') }}", "")

print(bill)
