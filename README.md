# ForecastApp: Demand estimation app
Application helps user to predict how much goods will be required on further periods based on known data.

## Manufacturing logistic background
In enterprise logistic there is need for estimation demand. To describe demand three models can be used: Brown model, Holt model and Winters model. Keeping order from simpliest which can describe one period further to more complicated models where additional parameters such as trend or seasonality are described.
## Implementation method
Project is an implementation of three mathematical models for demand estimation - Brown, Holt and Winters model. Implementation was written in Python 3.7 with usage of following packages:
- pandas (data processing and model build up)
- numpy (matrix calculations and data organisation)
- scipy (minimalization of objective function)
- matplotlib (visualisation of results, charts)
- tkinter (desktop graphical usage)<br>
## How to use App
1. Following packages are required: pandas, numpy, scipy, matplotlib, tkinter
2. Compile file: "Forecast_app.py"
3. Running app 
- Depending on the input data input choose one of following tab (1): Brown, Holt or Winters load data (2) in format provided in folder, data will be shown in table (3)
<br>(https://github.com/krzkub123/M.Sc.-code/blob/master/pic/image-1.png?raw=true)
-> In case of Winters model run window (1) to help check what kind of data (1) (additive or multiplicative) it is and choose Winters model (3;4). Input also Period length and overtake length (5)
<br>(https://user-images.githubusercontent.com/124029435/229750616-00f4ef72-ba8e-442e-828b-b2f99aed4c15.png)
- Run the analysis by clicking button (1), optimal coefficient of alpha, beta and gamma will be displayed (2). Results are for user interpretation (3).
<br>(https://github.com/krzkub123/M.Sc.-code/blob/master/pic/image-3.png?raw=true)