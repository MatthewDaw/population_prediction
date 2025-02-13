select
    CAST(year AS NUMERIC) as year,
    gender,
    age_group,
    metric,
    CAST(estimated_percent AS NUMERIC) as estimated_percent
from
    {{ ref('src_marriage_status') }}

