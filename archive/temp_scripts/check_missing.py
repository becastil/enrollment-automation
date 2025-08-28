import pandas as pd
from enrollment_automation_v6 import *

# Load data
plan_mappings = load_plan_mappings()
block_aggregations = load_block_aggregations()
df = read_and_prepare_data('data/input/source_data.xlsx', plan_mappings)
tier_data = build_tier_data_from_source(df, block_aggregations)

# Get total by client
source_totals = {}
for client_id, plans in tier_data.items():
    total = 0
    for plan_type, blocks in plans.items():
        for block_label, counts in blocks.items():
            total += sum(counts.values())
    if total > 0:
        source_totals[client_id] = total

# Check what's written
import csv
with open('output/write_log.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

written_totals = {}
for row in rows:
    if row['reason'] != 'duplicate':
        client_id = row['client_id']
        if client_id not in written_totals:
            written_totals[client_id] = 0
        written_totals[client_id] += int(row['value'])

print('Missing writes by client ID:')
total_missing = 0
for client_id, source_total in sorted(source_totals.items()):
    written_total = written_totals.get(client_id, 0)
    if written_total < source_total:
        missing = source_total - written_total
        total_missing += missing
        tab = CID_TO_TAB.get(client_id, 'UNKNOWN')
        print(f'  {client_id} ({tab:25s}): {missing:,} missing ({source_total:,} source vs {written_total:,} written)')

print(f'\nTotal missing: {total_missing:,}')
