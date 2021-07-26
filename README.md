# Airflow-Mini-Project

This mini project uses Apache Airflow to create a data pipeline that extracts online stock market
data from Yahoo Finance on AAPL and TSLA. The current script downloads the data using the yfinance package
and then computes the average price of each stock for the current date. This pipeline is scheduled to run
every weekday at 6:00 pm with maximum retries of 2 at 5 minute intervals. 

## Tasks in DAG
0. Creates temporary directory to store downloaded files from Yahoo Finance.
1. Downloads AAPL data.
2. Downloads TSLA data.
3. Move AAPL data to location query (task 5) will target.
4. Move TSLA data to location query (task 5) will target.
5. Query on market data. Currently takes average price from low, high, open, close, and close_adj prices and stores computed average in History.csv. 

![alt text](https://github.com/beatricetierra/Airflow-Mini-Project/blob/main/DAG_graphical_view.PNG)

**Fig 1. Graphical View of DAG tasks**

**[UPDATE 7/22/2021]**

After experiencing permission issues to move files in step 3 and 4, the following tasks were used:

0. Creates temporary directory to store downloaded files from Yahoo Finance. (Accesible using airflow user) 
1. Downloads AAPL data.
2. Downloads TSLA data.
3. Query on market data. Prints the stock ticket, timestamp, and the average price of the stock price (average of low, high, open, close, and close_adj prices). 

![alt text](https://github.com/beatricetierra/Airflow-Mini-Project/blob/main/DAG_graphical_view2.PNG)

**Fig 2. Updated Graphical View of DAG tasks**

## Set Up Procedure
1. Install Apache Airflow. 
    - For this project, Airflow was used with Docker. 
2. Save files in this repository in the same environment Airflow is setup. 
    - Make sure these files are saved in the 'dags' folder of airflow, or the folder set by the 'dags_folder' parameter in the airflow.cfg file.
3. [Optional] If using docker, run 'docker exec -it <container-name> bash' to open terminal of container airflow is running on. 
4. Run the command 'python SetupDAG.py'.
5. Run the command 'airflow scheduler'.
6. Run the command 'airflow dags list' to make sure dag 'marketvol' was scheduled correctly. 
