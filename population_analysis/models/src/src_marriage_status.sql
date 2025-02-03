WITH marriage_status AS (
    SELECT * FROM {{ ref('marriage_Status_2005_2017') }}
)

select * from marriage_status where metric != 'Total'

