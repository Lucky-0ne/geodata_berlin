# Energieverbrauch / Energy Consumption 2020 - 2022
- From Fisbroker
  - block of buildings granularity -> need preprocessing to plr...
  - Years 2020, 2021, 2022
  - Strom / Electricity
    - Energieverbrauch Strom je Gebäudeblock (Umweltatlas)
    - https://gdi.berlin.de/services/wfs/ua_stromverbrauch
  - Gasverbrauch / gas consumption
    - Energieverbrauch Gas je Gebäudeblock (Umweltatlas)
    - https://gdi.berlin.de/services/wfs/ua_gas
  - Fernwärme / district heating
    - Energieverbrauch - Fernwärme (Umweltatlas)
    - https://gdi.berlin.de/services/wfs/ua_fernwaerme

**ATTENTION: There are quite a few NaN values for building blocks for privacy reasons**, so beware this dataset might not be the most accurate on this fine granularity.  
From the WFS links above though, you can also download on district and postal code granularity, though I don't know if these coarser data sets are not simply a summary of the respective building block datasets...  
Percentage of blocks with nan consumption entries in the raw datasets:
| column name | nan percentage |
|:--------------------------|------:|
| district_heating_mwh_2022 | 85.19 |
| district_heating_mwh_2021 | 85.28 |
| district_heating_mwh_2020 | 85.52 |
| gas_mwh_2022              | 38.17 |
| gas_mwh_2021              | 34.51 |
| gas_mwh_2020              | 34.69 |
| electricity_mwh_2022      | 23.38 |
| electricity_mwh_2021      | 24.92 |
| electricity_mwh_2020      | 24.94 |

## Preprocessing
- Summarize from block of buildings granularity to plr granularity (spatial join)
  - first calculate centroid of block, then join with plr polygons worked best
- 