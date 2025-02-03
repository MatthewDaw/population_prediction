SELECT s.id as state_id, b.STATE, b.YEAR, b.BIRTHS
FROM {{ ref('src_birthrate') }} b
JOIN {{ ref('dim_state') }} s ON b.STATE = s.STATE_NAME
WHERE s.ID IS NOT NULL
