# Enrollment Data Processing Rules

**Version:** 1.0.0  
**Last Updated:** 2025-01-29  
**Workbook:** August (allowlisted 29 tabs)

---

## Executive Summary

This document defines how enrollment counts are produced from the source (Sheet1) and written to each tab in the August workbook. It covers the control checks, how plan codes map to plan types (EPO, VALUE, PPO where applicable), and per-tab aggregation and cell mappings. It also spells out multi-block facilities (sites with multiple EPO groupings) and the special 5-tier tabs that split **EE & Child** vs **EE & Children**.

---

## System Overview

1. **Inputs**

   * **Source table:** `Sheet1` containing member/coverage rows with at minimum: `CLIENT_ID`, `PLAN` (plan code), `BEN CODE` (or equivalent), and (for child split tabs) enough dependent info to determine exact child count where required.

2. **Transformations**

   * **Tier normalization:** Maps `BEN CODE` values to tier labels.
   * **Plan code classification:** Maps raw `PLAN` codes into plan **type** buckets (EPO, VALUE, PPO).
   * **Block aggregation:** On each allowed tab, roll up counts to its blocks, possibly splitting EPO into distinct union/variant blocks.

3. **Outputs**

   * Each tab's cells are populated according to its write map: a block (label) × tier grid with predefined cell addresses.

4. **Audit Trail**

   * A write log should include `(sheet, client_id, plan_type, block_label, tier, count, block_id)` and any diagnostics (e.g., unassigned plan codes).

---

## Control Totals & Validation Rules

* **Sheet allowlist (hard guard):** Only process the following 29 tabs. Any attempt to write to a non-allowlisted sheet fails.
* **Plan mapping integrity:** All distinct `PLAN` codes present in `Sheet1` must resolve to a plan type and, where applicable, to a block on the target tab. Unknowns are not allowed—fail with a mapping-gap report.
* **UNASSIGNED guard:** If any `PLAN` appears on a tab with block aggregation rules but does not appear in that tab's `sum_of` lists, fail with a table showing `(tab, client_id, plan_type, plan_code, count)`.
* **Dedupe key:** When writing, deduplicate on `(client_id, plan_type, block_label)` to allow multi-block EPO sites to display multiple blocks for the same plan type.
* **Post-write verification:** For every block, verify `aggregated source count == sum of cells written`.
* **Processed sheet tracking:** Mark a sheet as processed only if one or more **non-zero** writes occurred.
* **Tier label consistency:** Standard 4-tier labeling: `EE`, `EE & Spouse`, `EE & Children`, `EE & Family`. 5-tier tabs additionally include `EE & Child`.
* **Unrecognized client_id handling:** If a `CLIENT_ID` appears in Sheet1 but is not in the allowed client list for any tab, log a warning and exclude from processing.

---

## Plan Code Mappings (Classification)

> The following are seed rules (expand as needed). Value plan codes without facility suffixes are preferred over site-specific placeholders.

### Generic

* **VALUE:** `PRIMEMMVAL` + `PRIMEMMVALUE` (always summed when present)
* **EPO:** Codes beginning with `PRIMEMMEPO` (or site-specific EPO codes listed under each tab below)
* **PPO (where present):** Site-specific PPO codes (rare; some tabs include a PPO block)

### Multi-Block / Special Tabs (explicit mappings)

* **Encino–Garden Grove**

  * **H3250 Encino Hospital Medical Center**

    * *EPO — SEIU 121 RN:* `PRIMEMMEPOLEUN`
    * *EPO — Non-Union & SEIU-UHW unified:* `PRIMEMMEPO3` + `PRIMEMMEPOLE` + `PRIMEPOPRE21`
    * *VALUE:* `PRIMEMMVAL` + `PRIMEMMVALUE`
  * **H3260 Garden Grove Hospital Medical Center (incl. UNAC)**

    * *EPO — UNAC:* `PRIMEMMEPO3`
    * *EPO — Non-Union unified:* `PRIMEMMEPOLE` + `PRIMEPOPRE21`
    * *VALUE:* `PRIMEMMVAL` + `PRIMEMMVALUE`

* **St. Francis (H3275)**

  * *EPO — SEIU 2020 D1:* `PRIMESFSEEPO`
  * *EPO — UNAC D1:* `PRIMESFUNEPO`
  * *EPO — Non-Union D1:* `PRIMEMMSFEPO`
  * *VALUE:* `PRIMESFMCVAL`

* **Lower Bucks (H3330)**

  * *EPO — IUOE:* `PRIMEMMLBEPO`
  * *EPO — PASNAP & Non-Union:* `PRIMELBHEPO`
  * *VALUE (all):* `PRIMEMMVAL` + `PRIMEMMVALUE`

* **Saint Mary's Reno**

  * **H3395 Saint Mary's Regional Medical Center — Medical Group**

    * *EPO — Non-Union 2020 D2 unified:* `PRIMEMMSMMSMRMCEPO`
    * *EPO — CWA 2020 D2 unified:* `PRIMEMMSMECW`
    * *EPO — CNA 2019 D2 unified:* `PRIMEMMSMECN`
    * *VALUE:* `PRIMEMMVAL` + `PRIMEMMVALUE`

* **St. Michael's (H3530)**

  * *EPO — Non-Union:* `PRIMEMMSTEPO`
  * *EPO — CIR:* `PRIMEMMCIR`
  * *EPO — IUOE:* `PRIMEMMIUOE`
  * *EPO — JNESO:* `PRIMEMMJNESO`
  * *EPO — EPO PLUS (eff. 1/1/2023):* `PRIMEMMEPPLUS`
  * *VALUE:* `PRIMEMMVAL`

> **Note:** Some historical site-suffixed VALUE placeholders (e.g., `PRIMEMMWAVALUE`, `PRIMEMMNVVALUE`, etc.) are intentionally **NOT** used when the data provides the generic `PRIMEMMVAL/PRIMEMMVALUE` pair.

---

## Tier Normalization (BEN CODE → Tier)

* `EMP` → **EE** (EE Only)
* `ESP` → **EE & Spouse**
* `ECH` → **EE & Children** *(or split across EE & Child vs EE & Children on 5-tier tabs; see below)*
* `FAM` → **EE & Family**

### 5-Tier Handling (Encino–Garden Grove & North Vista only)

* **EE & Child:** Employees with **exactly 1** eligible child dependent.
* **EE & Children:** Employees with **2 or more** eligible child dependents.
* **Dependent whitelist** (counted as child): child, stepchild, adopted child, legal ward, foster child *(exclude spouse, self, parents, and other adult dependents).*
* **Fallback:** If dependent counts are unavailable, place **all** `ECH` into **EE & Children** and set **EE & Child** to 0 (log a warning).

---

## Allowed Tabs (29)

1. Centinela
2. Coshocton
3. Dallas Medical Center
4. Dallas Regional
5. East Liverpool
6. Encino-Garden Grove
7. Garden City
8. Harlingen
9. Illinois
10. Knapp
11. Lake Huron
12. Landmark
13. Legacy
14. Lower Bucks
15. Mission
16. Monroe
17. North Vista
18. Pampa
19. Providence & St John
20. Riverview & Gadsden
21. Roxborough
22. Saint Clare's
23. Saint Mary's Passaic
24. Saint Mary's Reno
25. Southern Regional
26. St Joe & St Mary's
27. St Michael's
28. St. Francis
29. Suburban

> **Name normalization:** Use these exact names when routing and writing. (E.g., "East Liverpool" not "East Liverpool City"; "Providence & St John" without a period.)

---

## Tab-by-Tab Rules (Cells, Blocks, Client IDs)

Below, each tab lists its client IDs, blocks (by plan type and label), and **cell mappings**. Tiers are assumed to be in **one column** and **consecutive rows** per block.

### Legacy

* **H3170 San Dimas Community Hospital**

  * EPO "San Dimas EPO" → G4:G7 (EE, EE&Sp, EE&Ch, EE&Fam)
  * VALUE "San Dimas VALUE" → G10:G13
* **H3130 Bio-Medical Services**

  * EPO "Bio-Med EPO" → G20:G23
  * VALUE "Bio-Med VALUE" → G26:G29
* **H3100 Chino Valley Medical Center**

  * EPO "Chino EPO" → G36:G39
  * VALUE "Chino VALUE" → G42:G45
* **H3300 Chino Valley Medical Center RNs**

  * EPO "Chino RN EPO" → G53:G56
  * VALUE "Chino RN VALUE" → G59:G62
* **H3140 Desert Valley Hospital**

  * EPO "Desert Valley EPO" → G69:G72
  * VALUE "Desert Valley VALUE" → G75:G78
* **H3150 Desert Valley Medical Group**

  * EPO "Desert Med EPO" → G85:G88
  * VALUE "Desert Med VALUE" → G91:G94
* **H3210 Huntington Beach Hospital**

  * EPO "Huntington EPO" → G101:G104
  * VALUE "Huntington VALUE" → G107:G110
* **H3200 La Palma Intercommunity Hospital**

  * EPO "La Palma EPO" → G133:G136
  * VALUE "La Palma VALUE" → G139:G142
* **H3160 Montclair Hospital Medical Center**

  * EPO "Montclair EPO" → G149:G152
  * VALUE "Montclair VALUE" → G155:G158
* **H3115 Premiere Healthcare Staffing**

  * EPO "Premiere EPO" → G165:G168
* **H3110 Prime Management Services**

  * EPO "Prime Mgmt EPO" → G175:G178
  * VALUE "Prime Mgmt VALUE" → G181:G184
* **H3230 Paradise Valley Hospital**

  * EPO "Paradise EPO" → G191:G194
  * VALUE "Paradise VALUE" → G197:G200
* **H3240 Paradise Valley Medical Group**

  * EPO "Paradise Med EPO" → G207:G210
  * VALUE "Paradise Med VALUE" → G213:G216
* **H3180 Sherman Oaks Hospital** *(multi-block: 2 EPO + 2 VALUE)*

  * EPO "Sherman EPO Block 1" → G223:G226
  * VALUE "Sherman VALUE Block 1" → G229:G232
  * EPO "Sherman EPO Block 2" → G239:G242
  * VALUE "Sherman VALUE Block 2" → G245:G248
* **H3220 West Anaheim Medical Center**

  * EPO "West Anaheim EPO" → G255:G258
  * VALUE "West Anaheim VALUE" → G261:G264
* **H3280 Shasta Regional Medical Center**

  * EPO "Shasta EPO" → G271:G274
  * VALUE "Shasta VALUE" → G277:G280
* **H3285 Shasta Medical Group**

  * EPO "Shasta Med EPO" → G287:G290
  * VALUE "Shasta Med VALUE" → G293:G296

### Centinela

* **H3270 Centinela Hospital**

  * EPO "Centinela EPO" → D3:D6
  * PPO "Centinela PPO" → D9:D12
  * VALUE "Centinela VALUE" → D15:D18
* **H3271 Marina Del Rey Hospital**

  * EPO "Marina EPO" → D21:D24
  * PPO "Marina PPO" → D27:D30

### Encino–Garden Grove *(5 tiers on this tab)*

* **H3220 West Anaheim Medical Center**

  * EPO "West Anaheim EPO" → D3:D7 (EE, EE&Sp, **EE & Child**, **EE & Children**, EE&Fam)
  * VALUE "West Anaheim VALUE" → D10:D14 (same 5 tiers)
* **H3250 Encino Hospital Medical Center** *(multi-block: 2 EPO)*

  * EPO "Encino Non-Union/SEIU-UHW EPO" → D17:D21
  * EPO "Encino SEIU 121 RN EPO" → D24:D28
  * VALUE "Encino VALUE" → D31:D35
* **H3260 Garden Grove Hospital (incl. UNAC)** *(multi-block: 2 EPO)*

  * EPO "Garden Grove Non-Union EPO" → D38:D42
  * EPO "Garden Grove UNAC EPO" → D45:D49
  * VALUE "Garden Grove VALUE" → D52:D56

### St. Francis

* **H3275 St. Francis Medical Center** *(multi-block: 3 EPO)*

  * EPO "St Francis SEIU 2020 D1 EPO" → D3:D6
  * EPO "St Francis UNAC D1 EPO" → D9:D12
  * EPO "St Francis Non-Union D1 EPO" → D15:D18
  * VALUE "St Francis VALUE" → D21:D24
* **H3276 St. Francis Physician**

  * EPO "St Francis Phys EPO" → D27:D30
  * VALUE "St Francis Phys VALUE" → D33:D36

### Pampa

* **H3320 Pampa Community Hospital**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Roxborough

* **H3325 Roxborough Memorial Hospital**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Lower Bucks *(multi-block: 2 EPO)*

* **H3330 Lower Bucks Hospital**

  * EPO "PRIME EPO PLAN – IUOE" → D10:D13
  * EPO "PRIME EPO PLAN – PASNAP & Non-Union" → D16:D19
  * VALUE "PRIME VALUE PLAN" → D22:D25

### Dallas Medical Center

* **H3335**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Dallas Regional

* **H3337**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Harlingen

* **H3370**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Knapp

* **H3355 Knapp Medical Center**

  * EPO "Knapp Med EPO" → D3:D6
  * VALUE "Knapp Med VALUE" → D9:D12
* **H3360 Knapp Medical Group**

  * EPO "Knapp Group EPO" → D15:D18

### Monroe

* **H3397**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Saint Mary's Reno

* **H3394 Saint Mary's Regional Medical Center**

  * EPO "St Mary's Regional EPO" → D3:D6
  * PPO "St Mary's Regional PPO" → D9:D12
  * VALUE "St Mary's Regional VALUE" → D15:D18
* **H3395 Saint Mary's Medical Group**

  * EPO "St Mary's Group EPO" → D21:D24
  * VALUE "St Mary's Group VALUE" → D27:D30
* **H3396 Saint Mary's PT**

  * EPO "St Mary's PT EPO" → D33:D36

### North Vista *(5 tiers on this tab)*

* **H3398**

  * EPO "PRIME EPO PLAN" → D3:D7
  * VALUE "PRIME VALUE PLAN" → D10:D14

### Riverview & Gadsden

* **H3338 Riverview Regional Medical Center**

  * EPO "Riverview EPO" → D3:D6
  * PPO "Riverview PPO" → D9:D12
  * VALUE "Riverview VALUE" → D15:D18
* **H3339 Gadsden Regional Medical Center**

  * EPO "Gadsden EPO" → D21:D24
  * VALUE "Gadsden VALUE" → D27:D30

### Saint Clare's

* **H3500**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Landmark

* **H3392**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Saint Mary's Passaic

* **H3505**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Southern Regional

* **H3510**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### St Michael's *(multi-block: 2 EPO, 2 PPO)*

* **H3530 St. Michael's Medical Center**

  * EPO "St Michael's JNESO EPO" → D3:D6
  * EPO "St Michael's Non-Union EPO" → D9:D12
  * PPO "St Michael's JNESO PPO" → D15:D18
  * PPO "St Michael's Non-Union PPO" → D21:D24
  * VALUE "St Michael's VALUE" → D27:D30

### Mission

* **H3540**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Coshocton

* **H3591**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Suburban

* **H3598 Suburban Community Hospital**

  * EPO "Suburban Hosp EPO" → D3:D6
  * PPO "Suburban Hosp PPO" → D9:D12
  * VALUE "Suburban Hosp VALUE" → D15:D18
* **H3599 Suburban Community Physicians**

  * EPO "Suburban Phys EPO" → D21:D24

### Garden City

* **H3375 Garden City Hospital**

  * EPO "Garden City Hosp EPO" → D3:D6
  * PPO "Garden City Hosp PPO" → D9:D12
  * VALUE "Garden City Hosp VALUE" → D15:D18
* **H3380 Garden City Osteopathic**

  * EPO "Garden City Osteo EPO" → D21:D24
* **H3385 Garden City MSO**

  * EPO "Garden City MSO EPO" → D27:D30

### Lake Huron

* **H3381 Lake Huron Medical Center**

  * EPO "Lake Huron Med EPO" → D3:D6
  * PPO "Lake Huron Med PPO" → D9:D12
  * VALUE "Lake Huron Med VALUE" → D15:D18
* **H3382 Lake Huron Physicians**

  * EPO "Lake Huron Phys EPO" → D21:D24

### Providence & St John

* **H3340 Providence Medical Center**

  * EPO "Providence EPO" → D3:D6
  * PPO "Providence PPO" → D9:D12
  * VALUE "Providence VALUE" → D15:D18
* **H3345 St. John Medical Center**

  * EPO "St John EPO" → D21:D24
  * VALUE "St John VALUE" → D27:D30

### East Liverpool

* **H3592**

  * EPO "PRIME EPO PLAN" → D3:D6
  * VALUE "PRIME VALUE PLAN" → D9:D12

### Illinois *(framework in place; expand as facility list grows)*

* **H3605 Glendora Hospital (placeholder)**

  * EPO "Glendora Hosp EPO" → D3:D6
  * PPO "Glendora Hosp PPO" → D9:D12
  * VALUE "Glendora Hosp VALUE" → D15:D18
* **Additional IL facilities:** Add client IDs and cell blocks as they become available (H3615, H3625, H3630, H3635, H3645, H3655, H3660, H3665, H3670, H3675, H3680).

### St Joe & St Mary's *(Configuration pending - to be added when workbook layout is confirmed)*

* **Cell grid and client IDs:** To be confirmed from the workbook layout. Add when available.

---

## Multi-Block Facilities (Summary)

* **Encino–Garden Grove:** Encino (2 EPO), Garden Grove (2 EPO). 5-tier tab.
* **St. Francis:** 3 EPO blocks (SEIU, UNAC, Non-Union) + VALUE.
* **Lower Bucks:** 2 EPO blocks (IUOE; PASNAP & Non-Union) + VALUE.
* **St Michael's:** 2 EPO + 2 PPO + VALUE.
* **Legacy:** Sherman Oaks has 2×EPO + 2×VALUE blocks inside the Legacy tab.

---

## Special Cases

* **5-tier vs 4-tier:** Only **Encino–Garden Grove** and **North Vista** split `EE & Child` vs `EE & Children`. All other tabs are 4-tier.
* **Name alignment:** Sheet names must match the allowlist exactly; standardize tier labels to one style (`EE`, `EE & Spouse`, `EE & Children`, `EE & Family`; `EE & Child` only where applicable).
* **VALUE mapping:** Prefer generic `PRIMEMMVAL`/`PRIMEMMVALUE`. Do **not** require site-suffixed VALUE codes.

---

## Data Flow Diagram

```mermaid
flowchart LR
  A[Sheet1 Source Rows] --> B[Tier Normalization\n(BEN CODE → Tier)]
  B --> C[Plan Classification\n(PLAN → {EPO, VALUE, PPO})]
  C --> D{Tab is Allowlisted?}
  D -- No --> X[Skip / Fail]
  D -- Yes --> E[Block Aggregation\n(client_id, plan_type, block_label)]
  E --> F[UNASSIGNED Guard\n(mapping-gap report if any)]
  F --> G[Write to Cells\n(per tab write map)]
  G --> H[Post-write Verification\n(source vs sheet sums)]
  H --> I[Write Log + Diagnostics]
```

---

## Quick Reference Tables

### Tier Labels

| Code | Tier Label                                |
| ---- | ----------------------------------------- |
| EMP  | EE                                        |
| ESP  | EE & Spouse                               |
| ECH  | EE & Children *(or split on 5-tier tabs)* |
| FAM  | EE & Family                               |

### 5-Tier Tabs

* Encino–Garden Grove
* North Vista

### Multi-Block (EPO) Tabs

* Encino–Garden Grove (Encino: SEIU 121 RN; Non-Union/SEIU-UHW. Garden Grove: UNAC; Non-Union)
* St. Francis (SEIU, UNAC, Non-Union)
* Lower Bucks (IUOE; PASNAP & Non-Union)
* St Michael's (plus PPO blocks)
* Legacy → Sherman Oaks (2×EPO + 2×VALUE)

### Tabs with PPO Blocks

* Centinela
* Saint Mary's Reno
* Riverview & Gadsden
* St Michael's
* Suburban
* Garden City
* Lake Huron
* Providence & St John
* Illinois (Glendora placeholder)

---

## Glossary

| Abbreviation | Definition |
| ------------ | ---------- |
| **EPO** | Exclusive Provider Organization |
| **PPO** | Preferred Provider Organization |
| **VALUE** | Value-based insurance plan type |
| **EE** | Employee (in tier context) |
| **SEIU** | Service Employees International Union |
| **UNAC** | United Nurses Association of California |
| **UHW** | United Healthcare Workers |
| **CWA** | Communications Workers of America |
| **CNA** | California Nurses Association |
| **CIR** | Committee of Interns and Residents |
| **IUOE** | International Union of Operating Engineers |
| **JNESO** | Health Professionals and Allied Employees |
| **PASNAP** | Pennsylvania Association of Staff Nurses and Allied Professionals |
| **RN** | Registered Nurse |
| **D1/D2** | District 1/District 2 (union designations) |

---

## CSV Summary (Optional)

You can generate a machine-readable CSV with columns:

```
sheet,client_id,plan_type,block_label,block_id,tier,cell
```

Each row describes one cell for one block (e.g., `Encino-Garden Grove,H3250,EPO,Encino SEIU 121 RN EPO,EN_EPO_2,EE & Spouse,D25`).

---

## Open Items / To-Dos

* **St Joe & St Mary's:** Capture layout (cells and client IDs) and add write map.
* **Illinois:** Extend beyond H3605 as facility list finalizes.
* **Child split inputs:** Confirm dependent type whitelist in your raw data; implement fallback logging when dependent counts are incomplete.
* **Version control:** Establish change management process for updates to mappings and rules.