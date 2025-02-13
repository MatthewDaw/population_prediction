WITH birth_rate AS (
    SELECT * FROM {{ ref('birthrate_2007_2023') }}
)

select * from birth_rate where NOTES is null

