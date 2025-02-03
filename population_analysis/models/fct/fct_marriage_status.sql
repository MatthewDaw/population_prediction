select
    year,
    gender,
    age_group,
    metric,
    estimated_percent
from
    {{ ref('src_marriage_status') }}



