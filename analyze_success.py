import csv
from collections import defaultdict

# Get what was written
with open('output/write_log.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Sum by client
written_by_client = defaultdict(int)
for row in rows:
    if row['reason'] != 'duplicate':
        written_by_client[row['client_id']] += int(row['value'])

# Load tier data
from enrollment_automation_v6 import *
plan_mappings = load_plan_mappings()
block_aggregations = load_block_aggregations()
df = read_and_prepare_data('data/input/source_data.xlsx', plan_mappings)
tier_data = build_tier_data_from_source(df, block_aggregations)

# Get source totals
source_by_client = {}
for client_id, plans in tier_data.items():
    total = 0
    for plan_type, blocks in plans.items():
        for block_label, counts in blocks.items():
            total += sum(counts.values())
    if total > 0:
        source_by_client[client_id] = total

# Compare
print('Client ID success rates:')
print('='*60)
total_success = 0
total_source = 0
for client_id in sorted(source_by_client.keys()):
    source = source_by_client[client_id]
    written = written_by_client.get(client_id, 0)
    pct = (written / source * 100) if source > 0 else 0
    total_success += written
    total_source += source
    
    status = '✓' if pct == 100 else '⚠' if pct > 0 else '✗'
    tab = CID_TO_TAB.get(client_id, 'UNKNOWN')
    print(f'{client_id} ({tab:25s}): {status} {written:4d}/{source:4d} ({pct:5.1f}%)')

print('='*60)
print(f'Total: {total_success:,}/{total_source:,} ({total_success/total_source*100:.1f}%)')