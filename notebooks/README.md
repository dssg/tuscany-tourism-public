# Desriptive analytics of our database


## Data description

IP Probe data is provided by Vodafone Italy and kept on a AWS redshift server. The population contains foreigners (with a non Italian SIM card) who visited Tuscany between May 2017 - February 2018. It contains signalling traces (every 1 minute) between the cell tower and users’ devices. In total we analyzed the flow of over 9 million unique tourists, within the aforementioned 10 month period.

## Containts

This notebook contains the code and charts for:
- Top 20 countries of origin of visitors across all time
- Number of visitors in Tuscany and Florence by month
- Heatmaps of numbers of visitors per territory by season
- Number of days spent in Tuscany
- Ratio of number of visitors from the top five countries, by month


## How to run the notebook?

To run the notebooks, the conda environment and Jupyter Notebooks should be installed with Python 3.6<, and all packages at `../requirements.txt`. To set up a conda environment, see ['setting up the environment'](https://github.com/dssg/TPT_tourism/blob/master/README.md)
