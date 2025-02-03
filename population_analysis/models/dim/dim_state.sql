WITH states AS (
    SELECT 1 AS id, 'Alabama' AS state_name, 'AL' AS state_abbreviation UNION ALL
    SELECT 2, 'Alaska', 'AK' UNION ALL
    SELECT 3, 'Arizona', 'AZ' UNION ALL
    SELECT 4, 'Arkansas', 'AR' UNION ALL
    SELECT 5, 'California', 'CA' UNION ALL
    SELECT 6, 'Colorado', 'CO' UNION ALL
    SELECT 7, 'Connecticut', 'CT' UNION ALL
    SELECT 8, 'Delaware', 'DE' UNION ALL
    SELECT 9, 'Florida', 'FL' UNION ALL
    SELECT 10, 'Georgia', 'GA' UNION ALL
    SELECT 11, 'Hawaii', 'HI' UNION ALL
    SELECT 12, 'Idaho', 'ID' UNION ALL
    SELECT 13, 'Illinois', 'IL' UNION ALL
    SELECT 14, 'Indiana', 'IN' UNION ALL
    SELECT 15, 'Iowa', 'IA' UNION ALL
    SELECT 16, 'Kansas', 'KS' UNION ALL
    SELECT 17, 'Kentucky', 'KY' UNION ALL
    SELECT 18, 'Louisiana', 'LA' UNION ALL
    SELECT 19, 'Maine', 'ME' UNION ALL
    SELECT 20, 'Maryland', 'MD' UNION ALL
    SELECT 21, 'Massachusetts', 'MA' UNION ALL
    SELECT 22, 'Michigan', 'MI' UNION ALL
    SELECT 23, 'Minnesota', 'MN' UNION ALL
    SELECT 24, 'Mississippi', 'MS' UNION ALL
    SELECT 25, 'Missouri', 'MO' UNION ALL
    SELECT 26, 'Montana', 'MT' UNION ALL
    SELECT 27, 'Nebraska', 'NE' UNION ALL
    SELECT 28, 'Nevada', 'NV' UNION ALL
    SELECT 29, 'New Hampshire', 'NH' UNION ALL
    SELECT 30, 'New Jersey', 'NJ' UNION ALL
    SELECT 31, 'New Mexico', 'NM' UNION ALL
    SELECT 32, 'New York', 'NY' UNION ALL
    SELECT 33, 'North Carolina', 'NC' UNION ALL
    SELECT 34, 'North Dakota', 'ND' UNION ALL
    SELECT 35, 'Ohio', 'OH' UNION ALL
    SELECT 36, 'Oklahoma', 'OK' UNION ALL
    SELECT 37, 'Oregon', 'OR' UNION ALL
    SELECT 38, 'Pennsylvania', 'PA' UNION ALL
    SELECT 39, 'Rhode Island', 'RI' UNION ALL
    SELECT 40, 'South Carolina', 'SC' UNION ALL
    SELECT 41, 'South Dakota', 'SD' UNION ALL
    SELECT 42, 'Tennessee', 'TN' UNION ALL
    SELECT 43, 'Texas', 'TX' UNION ALL
    SELECT 44, 'Utah', 'UT' UNION ALL
    SELECT 45, 'Vermont', 'VT' UNION ALL
    SELECT 46, 'Virginia', 'VA' UNION ALL
    SELECT 47, 'Washington', 'WA' UNION ALL
    SELECT 48, 'West Virginia', 'WV' UNION ALL
    SELECT 49, 'Wisconsin', 'WI' UNION ALL
    SELECT 50, 'Wyoming', 'WY'
)
SELECT
    s.id,
    s.state_name,
    s.state_abbreviation,
    CASE
        WHEN s.state_name IN ('Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont') THEN 'NEW_ENGLAND_NSA'
        WHEN s.state_name IN ('New York', 'New Jersey', 'Pennsylvania') THEN 'MIDDLE_ATLANTIC_NSA'
        WHEN s.state_name IN ('Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri') THEN 'EAST_NORTH_CENTRAL_NSA'
        WHEN s.state_name IN ('North Carolina', 'South Carolina', 'Georgia', 'Florida') THEN 'SOUTH_ATLANTIC_NSA'
        WHEN s.state_name IN ('Alabama', 'Mississippi', 'Louisiana', 'Tennessee', 'Kentucky', 'West Virginia', 'Arkansas', 'Delaware', 'Maryland', 'Virginia') THEN 'EAST_SOUTH_CENTRAL_NSA'
        WHEN s.state_name IN ('North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Montana', 'Wyoming') THEN 'WEST_NORTH_CENTRAL_NSA'
        WHEN s.state_name IN ('Oklahoma', 'Texas', 'New Mexico', 'Arizona') THEN 'WEST_SOUTH_CENTRAL_NSA'
        WHEN s.state_name IN ('Idaho', 'Utah', 'Nevada', 'Colorado', 'Arizona') THEN 'MOUNTAIN_NSA'
        WHEN s.state_name IN ('California', 'Oregon', 'Washington') THEN 'PACIFIC_NSA'
        WHEN s.state_name IN ('Alaska', 'Hawaii') THEN 'PACIFIC_SA'
        ELSE 'UNKNOWN_REGION'
    END AS region
FROM states s
