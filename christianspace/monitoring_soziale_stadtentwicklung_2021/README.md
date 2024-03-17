# Monitoring Soziale Stadtentwicklung 2021
The Monitoring of Social Urban Development (MSS) serves the detailed observation of changes in the socio-structural development in the subareas of the city of Berlin.  

- main page: https://www.berlin.de/sen/sbw/stadtdaten/stadtwissen/monitoring-soziale-stadtentwicklung/bericht-2021/
- PLR granularity
- features such as
  - unemployment
  - social benefits
  - child poverty
  - foreigners
  - public living spaces
  - respective dynamics
  - ...
- There are approx 10 PLR (i.e. nan rows) with invalid entries (not enough inhabitants)
- **detailed feature description** [**here**](https://www.berlin.de/sen/sbw/_assets/stadtdaten/stadtwissen/monitoring-soziale-stadtentwicklung/bericht-2021/mss_2021_indikatorenheft_fortschreibung_langfassung.pdf?ts=1705017669)

## Files
- `mss_2021.csv`: all features described in the features section but K08, K14, and K15 ("new" PLR convention with 542 areas)
- `mss_2021_easy.csv`: same as above, but with easier understood feature naming convention
- `mss_2021_k_08_14_15.csv`: K08, K14, and K15 ("old" PLR convention with 447 areas)

## Source
- MSS is split over multiple files and can be downloaded [here](https://www.berlin.de/sen/sbw/stadtdaten/stadtwissen/monitoring-soziale-stadtentwicklung/bericht-2021/tabellen/#Index)
- raw data was actually downloaded via [FISBroker](https://fbinter.stadt-berlin.de/fb/) utilizing following WFS connection URLs
  - https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_IndexInd_MSS2021_homogen
  - https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_Indizes_MSS2021_homogen
  - https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_KontextInd447_MSS2021_homogen (**Beware, incompatible PLR format, see Features**)
  - https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_KontextInd_MSS2021_homogen

## Features
**Features KI_08, KI_14, and KI_15 follow spatial conventions of old PLR schema. Do not merge the dataset `mss_2021_kontext_indikatoren_k08_k14_k15.csv` with the other sets!**

- PLR_ID: Planungsraum identifier
- EW: Einwohnerzahl / total population of PLR
- BEZ_ID: Bezirks / district identifier
- Status-Indikatoren
  - S1: Arbeitslosigkeit / unemployment in percent
  - S3: Transferbezug / social benefits receivers in percent
  - S4: Kinderarmut / child poverty in percent
  - D1: change in unemployment over two years in percent
  - D3: change in social benefits receivers over two years in percent
  - D4: change in child poverty over two years in percent
- Indizes 
  - Statusindex
    - SI_N: 1, 2, 3, 4
    - SI_V: hoch, mittel, niedrig, sehr niedrig
  - Dynamikindex
    - DI_N: 1, 3, 5
    - DI_V: positiv, stabil, negativ
  - SDI_V: "Status hoch, Dynamik positiv", "Status hoch, Dynamik stabil", ..., "Status sehr niedrig, Dynamik negativ"
- Kontext-Indikatoren KI_*, where * is:
  - 01: Jugendarbeitslosigkeit / youth unemployment
  - 02: Alleinerziehende / single parents
  - 03: Alterarmut / old age poverty
  - 04: Kinder und Jugendliche mit Migrationshintergrund / Children and adolescents with a migration background
  - 05 EinwohnerInnen mit Migrationshintergrund / Residents with a migration background
  - 16: AusländerInnen / foreigners
  - 06: change of 16 over two years
  - 17: Nicht-EU-AusländerInnen / Non-EU foreigners
  - 07: Ausländische Transferbeziehende (SGB II) / Foreign transfer recipients (SGB II)
  - (08: Städtische Wohnungen / Municipal apartments percentage of municipal apartments (housing units) of state-owned housing companies out of all apartments)
  - 09: Einwohnerinnen und Einwohner in einfacher Wohnlage / Residents in simple living conditions (Percentage of residents in simple living conditions including noise pollution from road traffic out of all residents)
  - 10: Wohndauer über fünf Jahre / Residence duration over five years
  - 11: Wanderungsvolumen innerhalb von zwei Jahren / Migration volume within two years (Average migration volume (arrivals plus departures per 100 residents) within two years in percent per year)
  - 12: Wanderungssaldo gesamt innerhalb von zwei Jahren / Total migration balance within two years (Average migration balance (arrivals minus departures per 100 residents) within two years in percent per year)
  - 13: Wanderungssaldo Kinder unter 6 Jahre innerhalb von zwei Jahren / Migration balance of children under 6 years within two years Average migration balance of children under 6 (arrivals minus departures of under 6-year-olds per 100 residents under six years) within two years in percent per year  
  - (14: Wohnräume / Average number of living spaces (incl. kitchen) per resident)
  - (15: Wohnfläche / Average living space in square meters per resident)

## Preprocessing
- For all subsets
  - Drop columns that are all nan
  - Remove PLR rows with nan entries (not enough residents...)
  - Create list of relevant features
- Join all features except KI_08, KI_14, and KI_15 to the file `mss_2021.csv`
- Safe KI_08, KI_14, and KI_15 to `mss_2021_k_08_14_15.csv`