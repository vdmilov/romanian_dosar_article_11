# About

Web parser for Romanian citizenship by descent (Article 11).
 
## Description
This project aims to provide a more efficient and error-free way to process and visualize data related to the Romanian citizenship by descent (Article 11) application process. The current process involves manual downloading and reading of PDF files published on the Ministry of Justice [website](http://cetatenie.just.ro/stadiu-dosar/), which can be time-consuming and prone to errors.

To solve this issue, this project automates the process of downloading, reading, and transforming the PDF files into a pandas DataFrame. The resulting data is then used to create a dashboard in Tableau for easy visualization and analysis of the data.

The goal is to update the dashboard on a monthly basis to keep track of the progress of the citizenship application process.
 
## Dashboard
Here is the final [dashboard](https://public.tableau.com/app/profile/vdmilov/viz/RomanianCitizenship/Dashboard1).

## Technologies used

- **[selenium](https://pypi.org/project/selenium/)**: Used for downloading the PDF files from the official website.
- **[tabula-py](https://pypi.org/project/tabula-py/)**: Used for scanning the PDF files and extracting the relevant data from them.
- **[pandas](https://pandas.pydata.org/)**: Used for transforming the extracted data into a structured format that can be used for analysis and visualization.
