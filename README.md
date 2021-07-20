# Airflow-Mini-Project

This mini project uses Apache Airflow to create a data pipeline that extracts online stock market
data from Yahoo Finance on AAPL and TSLA. The current script downloads the data using the yfinance package
and then computes the average price of each stock for the current date. This pipeline is scheduled to run
every weekday at 6:00 pm with maximum retries of 2 at 5 minute intervals. 

## Set Up Procedure
1. Install Apache Airflow. 
    - For this project, Airflow was used with Docker. 
2. Save files in this repository in the same environment Airflow is setup. 
    - Make sure these files are saved in the 'dags' folder of airflow, or the folder set by the 'dags_folder' parameter in the airflow.cfg file.
3. [Optional] If using docker, run 'docker exec -it <container-name> bash' to open terminal of container airflow is running on. 
4. Run the command 'python SetupDAG.py'.
5. Run the command 'airflow scheduler'.
6. Run the command 'airflow dags list' to make sure dag 'marketvol' was scheduled correctly. 
