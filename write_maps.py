"""
Write map definitions for all 29 allowlisted sheets
Each entry contains client_id, plan type, label, block_id, and cell mappings
"""

# Complete write maps for all sheets

LEGACY_WRITE_MAP = [
    # San Dimas Community Hospital — H3170
    {"client_id": "H3170", "plan": "EPO", "label": "San Dimas EPO", "block_id": "SD_EPO",
     "cells": {"EE": "G4", "EE+Spouse": "G5", "EE+Child(ren)": "G6", "EE+Family": "G7"}},
    {"client_id": "H3170", "plan": "VALUE", "label": "San Dimas VALUE", "block_id": "SD_VAL",
     "cells": {"EE": "G10", "EE+Spouse": "G11", "EE+Child(ren)": "G12", "EE+Family": "G13"}},
    
    # Bio-Medical Services — H3130
    {"client_id": "H3130", "plan": "EPO", "label": "Bio-Med EPO", "block_id": "BM_EPO",
     "cells": {"EE": "G20", "EE+Spouse": "G21", "EE+Child(ren)": "G22", "EE+Family": "G23"}},
    {"client_id": "H3130", "plan": "VALUE", "label": "Bio-Med VALUE", "block_id": "BM_VAL",
     "cells": {"EE": "G26", "EE+Spouse": "G27", "EE+Child(ren)": "G28", "EE+Family": "G29"}},
    
    # Chino Valley Medical Center — H3100
    {"client_id": "H3100", "plan": "EPO", "label": "Chino EPO", "block_id": "CH_EPO",
     "cells": {"EE": "G36", "EE+Spouse": "G37", "EE+Child(ren)": "G38", "EE+Family": "G39"}},
    {"client_id": "H3100", "plan": "VALUE", "label": "Chino VALUE", "block_id": "CH_VAL",
     "cells": {"EE": "G42", "EE+Spouse": "G43", "EE+Child(ren)": "G44", "EE+Family": "G45"}},
    
    # Chino Valley Medical Center RNs — H3300
    {"client_id": "H3300", "plan": "EPO", "label": "Chino RN EPO", "block_id": "CR_EPO",
     "cells": {"EE": "G53", "EE+Spouse": "G54", "EE+Child(ren)": "G55", "EE+Family": "G56"}},
    {"client_id": "H3300", "plan": "VALUE", "label": "Chino RN VALUE", "block_id": "CR_VAL",
     "cells": {"EE": "G59", "EE+Spouse": "G60", "EE+Child(ren)": "G61", "EE+Family": "G62"}},
    
    # Desert Valley Hospital — H3140
    {"client_id": "H3140", "plan": "EPO", "label": "Desert Valley EPO", "block_id": "DV_EPO",
     "cells": {"EE": "G69", "EE+Spouse": "G70", "EE+Child(ren)": "G71", "EE+Family": "G72"}},
    {"client_id": "H3140", "plan": "VALUE", "label": "Desert Valley VALUE", "block_id": "DV_VAL",
     "cells": {"EE": "G75", "EE+Spouse": "G76", "EE+Child(ren)": "G77", "EE+Family": "G78"}},
    
    # Desert Valley Medical Group — H3150
    {"client_id": "H3150", "plan": "EPO", "label": "Desert Med EPO", "block_id": "DM_EPO",
     "cells": {"EE": "G85", "EE+Spouse": "G86", "EE+Child(ren)": "G87", "EE+Family": "G88"}},
    {"client_id": "H3150", "plan": "VALUE", "label": "Desert Med VALUE", "block_id": "DM_VAL",
     "cells": {"EE": "G91", "EE+Spouse": "G92", "EE+Child(ren)": "G93", "EE+Family": "G94"}},
    
    # Huntington Beach Hospital — H3210
    {"client_id": "H3210", "plan": "EPO", "label": "Huntington EPO", "block_id": "HB_EPO",
     "cells": {"EE": "G101", "EE+Spouse": "G102", "EE+Child(ren)": "G103", "EE+Family": "G104"}},
    {"client_id": "H3210", "plan": "VALUE", "label": "Huntington VALUE", "block_id": "HB_VAL",
     "cells": {"EE": "G107", "EE+Spouse": "G108", "EE+Child(ren)": "G109", "EE+Family": "G110"}},
    
    # La Palma Intercommunity Hospital — H3200
    {"client_id": "H3200", "plan": "EPO", "label": "La Palma EPO", "block_id": "LP_EPO",
     "cells": {"EE": "G133", "EE+Spouse": "G134", "EE+Child(ren)": "G135", "EE+Family": "G136"}},
    {"client_id": "H3200", "plan": "VALUE", "label": "La Palma VALUE", "block_id": "LP_VAL",
     "cells": {"EE": "G139", "EE+Spouse": "G140", "EE+Child(ren)": "G141", "EE+Family": "G142"}},
    
    # Montclair Hospital Medical Center — H3160
    {"client_id": "H3160", "plan": "EPO", "label": "Montclair EPO", "block_id": "MC_EPO",
     "cells": {"EE": "G149", "EE+Spouse": "G150", "EE+Child(ren)": "G151", "EE+Family": "G152"}},
    {"client_id": "H3160", "plan": "VALUE", "label": "Montclair VALUE", "block_id": "MC_VAL",
     "cells": {"EE": "G155", "EE+Spouse": "G156", "EE+Child(ren)": "G157", "EE+Family": "G158"}},
    
    # Premiere Healthcare Staffing — H3115 (EPO only)
    {"client_id": "H3115", "plan": "EPO", "label": "Premiere EPO", "block_id": "PR_EPO",
     "cells": {"EE": "G165", "EE+Spouse": "G166", "EE+Child(ren)": "G167", "EE+Family": "G168"}},
    
    # Prime Management Services — H3110
    {"client_id": "H3110", "plan": "EPO", "label": "Prime Mgmt EPO", "block_id": "PM_EPO",
     "cells": {"EE": "G175", "EE+Spouse": "G176", "EE+Child(ren)": "G177", "EE+Family": "G178"}},
    {"client_id": "H3110", "plan": "VALUE", "label": "Prime Mgmt VALUE", "block_id": "PM_VAL",
     "cells": {"EE": "G181", "EE+Spouse": "G182", "EE+Child(ren)": "G183", "EE+Family": "G184"}},
    
    # Paradise Valley Hospital — H3230
    {"client_id": "H3230", "plan": "EPO", "label": "Paradise EPO", "block_id": "PV_EPO",
     "cells": {"EE": "G191", "EE+Spouse": "G192", "EE+Child(ren)": "G193", "EE+Family": "G194"}},
    {"client_id": "H3230", "plan": "VALUE", "label": "Paradise VALUE", "block_id": "PV_VAL",
     "cells": {"EE": "G197", "EE+Spouse": "G198", "EE+Child(ren)": "G199", "EE+Family": "G200"}},
    
    # Paradise Valley Medical Group — H3240
    {"client_id": "H3240", "plan": "EPO", "label": "Paradise Med EPO", "block_id": "PVM_EPO",
     "cells": {"EE": "G207", "EE+Spouse": "G208", "EE+Child(ren)": "G209", "EE+Family": "G210"}},
    {"client_id": "H3240", "plan": "VALUE", "label": "Paradise Med VALUE", "block_id": "PVM_VAL",
     "cells": {"EE": "G213", "EE+Spouse": "G214", "EE+Child(ren)": "G215", "EE+Family": "G216"}},
    
    # Sherman Oaks Hospital — H3180 (MULTI-BLOCK: 2 EPO + 2 VALUE)
    {"client_id": "H3180", "plan": "EPO", "label": "Sherman EPO Block 1", "block_id": "SO_EPO_1",
     "cells": {"EE": "G223", "EE+Spouse": "G224", "EE+Child(ren)": "G225", "EE+Family": "G226"}},
    {"client_id": "H3180", "plan": "VALUE", "label": "Sherman VALUE Block 1", "block_id": "SO_VAL_1",
     "cells": {"EE": "G229", "EE+Spouse": "G230", "EE+Child(ren)": "G231", "EE+Family": "G232"}},
    {"client_id": "H3180", "plan": "EPO", "label": "Sherman EPO Block 2", "block_id": "SO_EPO_2",
     "cells": {"EE": "G239", "EE+Spouse": "G240", "EE+Child(ren)": "G241", "EE+Family": "G242"}},
    {"client_id": "H3180", "plan": "VALUE", "label": "Sherman VALUE Block 2", "block_id": "SO_VAL_2",
     "cells": {"EE": "G245", "EE+Spouse": "G246", "EE+Child(ren)": "G247", "EE+Family": "G248"}},
    
    # West Anaheim Medical Center — H3220 (Note: Also in Encino-Garden Grove)
    {"client_id": "H3220", "plan": "EPO", "label": "West Anaheim EPO", "block_id": "WA_EPO",
     "cells": {"EE": "G255", "EE+Spouse": "G256", "EE+Child(ren)": "G257", "EE+Family": "G258"}},
    {"client_id": "H3220", "plan": "VALUE", "label": "West Anaheim VALUE", "block_id": "WA_VAL",
     "cells": {"EE": "G261", "EE+Spouse": "G262", "EE+Child(ren)": "G263", "EE+Family": "G264"}},
    
    # Shasta Regional Medical Center — H3280
    {"client_id": "H3280", "plan": "EPO", "label": "Shasta EPO", "block_id": "SR_EPO",
     "cells": {"EE": "G271", "EE+Spouse": "G272", "EE+Child(ren)": "G273", "EE+Family": "G274"}},
    {"client_id": "H3280", "plan": "VALUE", "label": "Shasta VALUE", "block_id": "SR_VAL",
     "cells": {"EE": "G277", "EE+Spouse": "G278", "EE+Child(ren)": "G279", "EE+Family": "G280"}},
    
    # Shasta Medical Group — H3285
    {"client_id": "H3285", "plan": "EPO", "label": "Shasta Med EPO", "block_id": "SM_EPO",
     "cells": {"EE": "G287", "EE+Spouse": "G288", "EE+Child(ren)": "G289", "EE+Family": "G290"}},
    {"client_id": "H3285", "plan": "VALUE", "label": "Shasta Med VALUE", "block_id": "SM_VAL",
     "cells": {"EE": "G293", "EE+Spouse": "G294", "EE+Child(ren)": "G295", "EE+Family": "G296"}},
]

CENTINELA_WRITE_MAP = [
    # Centinela Hospital — H3270
    {"client_id": "H3270", "plan": "EPO", "label": "Centinela EPO", "block_id": "CE_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3270", "plan": "PPO", "label": "Centinela PPO", "block_id": "CE_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3270", "plan": "VALUE", "label": "Centinela VALUE", "block_id": "CE_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Marina Del Rey Hospital — H3271
    {"client_id": "H3271", "plan": "EPO", "label": "Marina EPO", "block_id": "MD_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3271", "plan": "PPO", "label": "Marina PPO", "block_id": "MD_PPO",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
]

ENCINO_GARDEN_GROVE_WRITE_MAP = [
    # West Anaheim Medical Center — H3220
    {"client_id": "H3220", "plan": "EPO", "label": "West Anaheim EPO", "block_id": "WA_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Child": "D5", "EE & Children": "D6", "EE & Family": "D7"}},
    {"client_id": "H3220", "plan": "VALUE", "label": "West Anaheim VALUE", "block_id": "WA_VAL",
     "cells": {"EE": "D10", "EE & Spouse": "D11", "EE & Child": "D12", "EE & Children": "D13", "EE & Family": "D14"}},
    
    # Encino Hospital Medical Center — H3250 (MULTI-BLOCK: 2 EPO)
    {"client_id": "H3250", "plan": "EPO", "label": "Encino Non-Union/SEIU-UHW EPO", "block_id": "EN_EPO_1",
     "cells": {"EE": "D17", "EE & Spouse": "D18", "EE & Child": "D19", "EE & Children": "D20", "EE & Family": "D21"}},
    {"client_id": "H3250", "plan": "EPO", "label": "Encino SEIU 121 RN EPO", "block_id": "EN_EPO_2",
     "cells": {"EE": "D24", "EE & Spouse": "D25", "EE & Child": "D26", "EE & Children": "D27", "EE & Family": "D28"}},
    {"client_id": "H3250", "plan": "VALUE", "label": "Encino VALUE", "block_id": "EN_VAL",
     "cells": {"EE": "D31", "EE & Spouse": "D32", "EE & Child": "D33", "EE & Children": "D34", "EE & Family": "D35"}},
    
    # Garden Grove Hospital — H3260 (MULTI-BLOCK: 2 EPO)
    {"client_id": "H3260", "plan": "EPO", "label": "Garden Grove Non-Union EPO", "block_id": "GG_EPO_1",
     "cells": {"EE": "D38", "EE & Spouse": "D39", "EE & Child": "D40", "EE & Children": "D41", "EE & Family": "D42"}},
    {"client_id": "H3260", "plan": "EPO", "label": "Garden Grove UNAC EPO", "block_id": "GG_EPO_2",
     "cells": {"EE": "D45", "EE & Spouse": "D46", "EE & Child": "D47", "EE & Children": "D48", "EE & Family": "D49"}},
    {"client_id": "H3260", "plan": "VALUE", "label": "Garden Grove VALUE", "block_id": "GG_VAL",
     "cells": {"EE": "D52", "EE & Spouse": "D53", "EE & Child": "D54", "EE & Children": "D55", "EE & Family": "D56"}},
]

ST_FRANCIS_WRITE_MAP = [
    # St. Francis Medical Center — H3275 (MULTI-BLOCK: 3 EPO)
    {"client_id": "H3275", "plan": "EPO", "label": "St Francis SEIU 2020 D1 EPO", "block_id": "SF_EPO_1",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3275", "plan": "EPO", "label": "St Francis UNAC D1 EPO", "block_id": "SF_EPO_2",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3275", "plan": "EPO", "label": "St Francis Non-Union D1 EPO", "block_id": "SF_EPO_3",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    {"client_id": "H3275", "plan": "VALUE", "label": "St Francis VALUE", "block_id": "SF_VAL",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    
    # St Francis Physician — H3276
    {"client_id": "H3276", "plan": "EPO", "label": "St Francis Phys EPO", "block_id": "SFP_EPO",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
    {"client_id": "H3276", "plan": "VALUE", "label": "St Francis Phys VALUE", "block_id": "SFP_VAL",
     "cells": {"EE": "D33", "EE & Spouse": "D34", "EE & Children": "D35", "EE & Family": "D36"}},
]

PAMPA_WRITE_MAP = [
    # Pampa Community Hospital — H3320
    {"client_id": "H3320", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "PA_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3320", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "PA_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

ROXBOROUGH_WRITE_MAP = [
    # Roxborough Memorial Hospital — H3325
    {"client_id": "H3325", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "RX_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3325", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "RX_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

LOWER_BUCKS_WRITE_MAP = [
    # Lower Bucks Hospital — H3330 (MULTI-BLOCK: 2 EPO)
    {"client_id": "H3330", "plan": "EPO", "label": "PRIME EPO PLAN - IUOE", "block_id": "LB_EPO_IUOE",
     "cells": {"EE": "D10", "EE & Spouse": "D11", "EE & Children": "D12", "EE & Family": "D13"}},
    {"client_id": "H3330", "plan": "EPO", "label": "PRIME EPO PLAN - PASNAP & Non-Union", "block_id": "LB_EPO_PASNAP",
     "cells": {"EE": "D16", "EE & Spouse": "D17", "EE & Children": "D18", "EE & Family": "D19"}},
    {"client_id": "H3330", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "LB_VAL",
     "cells": {"EE": "D22", "EE & Spouse": "D23", "EE & Children": "D24", "EE & Family": "D25"}}
]

DALLAS_MEDICAL_CENTER_WRITE_MAP = [
    {"client_id": "H3335", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "DM_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3335", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "DM_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

DALLAS_REGIONAL_WRITE_MAP = [
    {"client_id": "H3337", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "DR_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3337", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "DR_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

HARLINGEN_WRITE_MAP = [
    {"client_id": "H3370", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "HA_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3370", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "HA_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

KNAPP_WRITE_MAP = [
    # Knapp Medical Center — H3355
    {"client_id": "H3355", "plan": "EPO", "label": "Knapp Med EPO", "block_id": "KM_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3355", "plan": "VALUE", "label": "Knapp Med VALUE", "block_id": "KM_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    
    # Knapp Medical Group — H3360
    {"client_id": "H3360", "plan": "EPO", "label": "Knapp Group EPO", "block_id": "KG_EPO",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
]

MONROE_WRITE_MAP = [
    {"client_id": "H3397", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "MO_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3397", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "MO_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

SAINT_MARYS_RENO_WRITE_MAP = [
    # Saint Mary's Regional Medical Center — H3394
    {"client_id": "H3394", "plan": "EPO", "label": "St Mary's Regional EPO", "block_id": "SMR_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3394", "plan": "PPO", "label": "St Mary's Regional PPO", "block_id": "SMR_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3394", "plan": "VALUE", "label": "St Mary's Regional VALUE", "block_id": "SMR_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Saint Mary's Medical Group — H3395
    {"client_id": "H3395", "plan": "EPO", "label": "St Mary's Group EPO", "block_id": "SMG_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3395", "plan": "VALUE", "label": "St Mary's Group VALUE", "block_id": "SMG_VAL",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
    
    # Saint Mary's PT — H3396
    {"client_id": "H3396", "plan": "EPO", "label": "St Mary's PT EPO", "block_id": "SMP_EPO",
     "cells": {"EE": "D33", "EE & Spouse": "D34", "EE & Children": "D35", "EE & Family": "D36"}},
]

NORTH_VISTA_WRITE_MAP = [
    # North Vista Hospital — H3398 (CHILD SPLIT TAB)
    {"client_id": "H3398", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "NV_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Child": "D5", "EE & Children": "D6", "EE & Family": "D7"}},
    {"client_id": "H3398", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "NV_VAL",
     "cells": {"EE": "D10", "EE & Spouse": "D11", "EE & Child": "D12", "EE & Children": "D13", "EE & Family": "D14"}}
]

RIVERVIEW_GADSDEN_WRITE_MAP = [
    # Riverview Regional Medical Center — H3338
    {"client_id": "H3338", "plan": "EPO", "label": "Riverview EPO", "block_id": "RV_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3338", "plan": "PPO", "label": "Riverview PPO", "block_id": "RV_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3338", "plan": "VALUE", "label": "Riverview VALUE", "block_id": "RV_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Gadsden Regional Medical Center — H3339
    {"client_id": "H3339", "plan": "EPO", "label": "Gadsden EPO", "block_id": "GA_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3339", "plan": "VALUE", "label": "Gadsden VALUE", "block_id": "GA_VAL",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
]

SAINT_CLARES_WRITE_MAP = [
    {"client_id": "H3500", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "SC_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3500", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "SC_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

LANDMARK_WRITE_MAP = [
    {"client_id": "H3392", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "LM_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3392", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "LM_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

SAINT_MARYS_PASSAIC_WRITE_MAP = [
    {"client_id": "H3505", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "SMP_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3505", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "SMP_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

SOUTHERN_REGIONAL_WRITE_MAP = [
    {"client_id": "H3510", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "SO_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3510", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "SO_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

ST_MICHAELS_WRITE_MAP = [
    # St. Michael's Medical Center — H3530 (MULTI-BLOCK: 2 EPO, 2 PPO)
    {"client_id": "H3530", "plan": "EPO", "label": "St Michael's JNESO EPO", "block_id": "SM_EPO_JNESO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3530", "plan": "EPO", "label": "St Michael's Non-Union EPO", "block_id": "SM_EPO_NU",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3530", "plan": "PPO", "label": "St Michael's JNESO PPO", "block_id": "SM_PPO_JNESO",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    {"client_id": "H3530", "plan": "PPO", "label": "St Michael's Non-Union PPO", "block_id": "SM_PPO_NU",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3530", "plan": "VALUE", "label": "St Michael's VALUE", "block_id": "SM_VAL",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}}
]

MISSION_REGIONAL_WRITE_MAP = [
    {"client_id": "H3540", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "MR_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3540", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "MR_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

COSHOCTON_COUNTY_WRITE_MAP = [
    {"client_id": "H3591", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "CO_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3591", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "CO_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

SUBURBAN_COMMUNITY_WRITE_MAP = [
    # Suburban Community Hospital — H3598
    {"client_id": "H3598", "plan": "EPO", "label": "Suburban Hosp EPO", "block_id": "SH_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3598", "plan": "PPO", "label": "Suburban Hosp PPO", "block_id": "SH_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3598", "plan": "VALUE", "label": "Suburban Hosp VALUE", "block_id": "SH_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Suburban Community Physicians — H3599
    {"client_id": "H3599", "plan": "EPO", "label": "Suburban Phys EPO", "block_id": "SP_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
]

GARDEN_CITY_WRITE_MAP = [
    # Garden City Hospital — H3375
    {"client_id": "H3375", "plan": "EPO", "label": "Garden City Hosp EPO", "block_id": "GCH_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3375", "plan": "PPO", "label": "Garden City Hosp PPO", "block_id": "GCH_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3375", "plan": "VALUE", "label": "Garden City Hosp VALUE", "block_id": "GCH_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Garden City Osteopathic — H3380
    {"client_id": "H3380", "plan": "EPO", "label": "Garden City Osteo EPO", "block_id": "GCO_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    
    # Garden City MSO — H3385
    {"client_id": "H3385", "plan": "EPO", "label": "Garden City MSO EPO", "block_id": "GCM_EPO",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
]

LAKE_HURON_WRITE_MAP = [
    # Lake Huron Medical Center — H3381
    {"client_id": "H3381", "plan": "EPO", "label": "Lake Huron Med EPO", "block_id": "LHM_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3381", "plan": "PPO", "label": "Lake Huron Med PPO", "block_id": "LHM_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3381", "plan": "VALUE", "label": "Lake Huron Med VALUE", "block_id": "LHM_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Lake Huron Physicians — H3382
    {"client_id": "H3382", "plan": "EPO", "label": "Lake Huron Phys EPO", "block_id": "LHP_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
]

PROVIDENCE_ST_JOHN_WRITE_MAP = [
    # Providence Medical Center — H3340
    {"client_id": "H3340", "plan": "EPO", "label": "Providence EPO", "block_id": "PR_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3340", "plan": "PPO", "label": "Providence PPO", "block_id": "PR_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3340", "plan": "VALUE", "label": "Providence VALUE", "block_id": "PR_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # St. John Medical Center — H3345
    {"client_id": "H3345", "plan": "EPO", "label": "St John EPO", "block_id": "SJ_EPO",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3345", "plan": "VALUE", "label": "St John VALUE", "block_id": "SJ_VAL",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}},
]

EAST_LIVERPOOL_CITY_WRITE_MAP = [
    {"client_id": "H3592", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "EL_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3592", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "EL_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

OHIO_VALLEY_HHC_WRITE_MAP = [
    {"client_id": "H3594", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "OV_VAL",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}}
]

RIVER_VALLEY_PRI_WRITE_MAP = [
    {"client_id": "H3595", "plan": "EPO", "label": "PRIME EPO PLAN", "block_id": "RVP_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3595", "plan": "VALUE", "label": "PRIME VALUE PLAN", "block_id": "RVP_VAL",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}}
]

ST_MARYS_MEDICAL_WRITE_MAP = [
    # St. Mary's Medical Center — H3596 (MULTI-BLOCK: 2 EPO, 2 PPO)
    {"client_id": "H3596", "plan": "EPO", "label": "St Mary's CIR EPO", "block_id": "STM_EPO_CIR",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3596", "plan": "EPO", "label": "St Mary's Non-Union EPO", "block_id": "STM_EPO_NU",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3596", "plan": "PPO", "label": "St Mary's CIR PPO", "block_id": "STM_PPO_CIR",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    {"client_id": "H3596", "plan": "PPO", "label": "St Mary's Non-Union PPO", "block_id": "STM_PPO_NU",
     "cells": {"EE": "D21", "EE & Spouse": "D22", "EE & Children": "D23", "EE & Family": "D24"}},
    {"client_id": "H3596", "plan": "VALUE", "label": "St Mary's VALUE", "block_id": "STM_VAL",
     "cells": {"EE": "D27", "EE & Spouse": "D28", "EE & Children": "D29", "EE & Family": "D30"}}
]

ILLINOIS_WRITE_MAP = [
    # Multiple Illinois facilities (H3605-H3680)
    {"client_id": "H3605", "plan": "EPO", "label": "Glendora Hosp EPO", "block_id": "GL_EPO",
     "cells": {"EE": "D3", "EE & Spouse": "D4", "EE & Children": "D5", "EE & Family": "D6"}},
    {"client_id": "H3605", "plan": "PPO", "label": "Glendora Hosp PPO", "block_id": "GL_PPO",
     "cells": {"EE": "D9", "EE & Spouse": "D10", "EE & Children": "D11", "EE & Family": "D12"}},
    {"client_id": "H3605", "plan": "VALUE", "label": "Glendora Hosp VALUE", "block_id": "GL_VAL",
     "cells": {"EE": "D15", "EE & Spouse": "D16", "EE & Children": "D17", "EE & Family": "D18"}},
    
    # Add other Illinois facilities here as needed
    # H3615, H3625, H3630, H3635, H3645, H3655, H3660, H3665, H3670, H3675, H3680
]

# Dictionary to map sheet names to their write maps
SHEET_WRITE_MAPS = {
    'Legacy': LEGACY_WRITE_MAP,
    'Centinela': CENTINELA_WRITE_MAP,
    'Encino-Garden Grove': ENCINO_GARDEN_GROVE_WRITE_MAP,
    'St. Francis': ST_FRANCIS_WRITE_MAP,
    'Pampa': PAMPA_WRITE_MAP,
    'Roxborough': ROXBOROUGH_WRITE_MAP,
    'Lower Bucks': LOWER_BUCKS_WRITE_MAP,
    'Dallas Medical Center': DALLAS_MEDICAL_CENTER_WRITE_MAP,
    'Dallas Regional': DALLAS_REGIONAL_WRITE_MAP,
    'Harlingen': HARLINGEN_WRITE_MAP,
    'Knapp': KNAPP_WRITE_MAP,
    'Monroe': MONROE_WRITE_MAP,
    "Saint Mary's Reno": SAINT_MARYS_RENO_WRITE_MAP,
    'North Vista': NORTH_VISTA_WRITE_MAP,
    'Riverview & Gadsden': RIVERVIEW_GADSDEN_WRITE_MAP,
    "Saint Clare's": SAINT_CLARES_WRITE_MAP,
    'Landmark': LANDMARK_WRITE_MAP,
    "Saint Mary's Passaic": SAINT_MARYS_PASSAIC_WRITE_MAP,
    'Southern Regional': SOUTHERN_REGIONAL_WRITE_MAP,
    "St. Michael's": ST_MICHAELS_WRITE_MAP,
    'Mission Regional': MISSION_REGIONAL_WRITE_MAP,
    'Coshocton County': COSHOCTON_COUNTY_WRITE_MAP,
    'Suburban Community': SUBURBAN_COMMUNITY_WRITE_MAP,
    'Garden City': GARDEN_CITY_WRITE_MAP,
    'Lake Huron': LAKE_HURON_WRITE_MAP,
    'Providence & St. John': PROVIDENCE_ST_JOHN_WRITE_MAP,
    'East Liverpool City': EAST_LIVERPOOL_CITY_WRITE_MAP,
    'Ohio Valley HHC': OHIO_VALLEY_HHC_WRITE_MAP,
    'River Valley Pri.': RIVER_VALLEY_PRI_WRITE_MAP,
    "St. Mary's Medical": ST_MARYS_MEDICAL_WRITE_MAP,
    'Illinois': ILLINOIS_WRITE_MAP,
    # Note: "St. Joe & St. Mary's" needs to be added when cell mappings are known
}