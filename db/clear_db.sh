influx delete \
  --bucket patient_measurements \
  --start 1970-01-01T00:00:00Z \
  --stop $(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --predicate '_measurement="bpm"'

 influx delete \
  --bucket patient_measurements \
  --start 1970-01-01T00:00:00Z \
  --stop $(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --predicate '_measurement="temp"'
