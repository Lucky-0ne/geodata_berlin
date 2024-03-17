# Monitoring Gewaltdelinquenz / Violent Delinquency
Violent delinquency is divided into three themes: - Youth violence, - Domestic and partnership violence, - Total violent offenses. The data come from the Berlin Monitoring of Violent Delinquency and reflect the recorded violent offenses in terms of violence exposure by standard deviation at the level of Life-World Oriented Spaces (LOR).

- Granularity: PLR (new LOR)
- Verbose documentation on data [here](https://camino-werkstatt.de/downloads/Berliner-Monitoring-Gewaltdelinquenz-2023-Teil-1.pdf)
- Fisbroker download WFS URL: https://gdi.berlin.de/services/wfs/gewaltdelinquenz (3 datasets)
  - overall violence
  - youth violence
  - domestic and partnershop

## Files
- `violent_delinquency.csv`
- `violent_delinquency_easy.csv`: Contains only verbally encoded features

## Features
- PLR_NAME
- PLR_ID
- *_n for numeric, *_v for verbal
  - overall_n
  - overall_v
  - innerfam_partner_n
  - innerfam_partner_v
  - youth_n
  - youth_v

The features are 0...4 in the numeric case, where
- 0: mostly uninhabited (verbal: Weitgehend unbewohnte Fläche)
- 1: low (verbal: Niedrig)
- 2: middle (verbal: Mittel)
- 3: high (verbal: Erhöht)
- 4: very high (veral: Stark erhöht)

## Preprocessing
Here we only needed to split one column in two and merge the single datasets...