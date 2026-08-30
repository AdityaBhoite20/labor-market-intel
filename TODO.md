# Future Enhancements

- Add metro-area level LAUS data (e.g. Seattle, Austin, SF) once core pipeline is stable
- Consider dynamic OEWS year detection instead of hardcoded "2025"
- Add BLS Employment projections as a real future data source for te "projected-growth" angle

## Known Data Limitations
- SOC code reclassifications between 2020-2025 (e.g. Data Scientists: 15-2098 in 2020 → 15-2051 from ~2021 onward) mean some occupations are excluded from year-over-year growth comparisons via simple SOC-code joins. A more robust approach would map old→new SOC codes using BLS's official crosswalk file before comparing across years.