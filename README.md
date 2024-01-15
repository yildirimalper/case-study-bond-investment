# Bond Investment Strategy - Case Study

```plain
├── original_data/
|   ├── bonds.xlsx
|   ├── cds_by_countries.xlsx
|   ├── missing_issuers_country_pairings.xlsx
├── processed_data/
|   ├── bonds-data.xlsx
├── utils/
|   ├── bond_math.py
|   ├── correct_avg_and_3m.py
|   ├── get_country.py
├── assets/
|   ├── yield_curve.png
├── data_cleaning.py
├── bond-strategy-presentation.pptx
├── bond-strategy-presentation.pdf
├── environment.yml
├── README.md
```

### Notes on Installation

To clone this repository in your local machine,

```shell
git clone https://github.com/yildirimalper/case-study-bond-investment
```

After cloning repository, by using the `environment.yml` file, you can recreate the exact environment required for the project with:

```shell
conda env create -f environment.yml
conda activate bond-case-study
```