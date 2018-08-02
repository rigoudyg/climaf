cLinearRegression : performs a linear regression between X and Y
---------------------------------------------------

cLinearRegression performs a linear regression Y = aX + b between two fields X and Y. They can be either spatio-temporal fields (same grids) or just time series. Y can be a spatio-temporal field, and X can be a time series.
This operator is based on cdutil (CDAT).

**References** : https://uvcdat.llnl.gov/

**Provider / contact** : climaf at meteo dot fr

**Inputs** (in the order of CliMAF call):
  - X: either a spatio-temporal field or a time series
  - Y: either a spatio-temporal field or time series of same dimension as X; if X is a spatio-temporal field, Y can't be a time series

**Mandatory arguments**:
  None

**Optional arguments**:
  None

**Output** : the slope a of the linear regression (either a field, or one value)

**Climaf call example** ::
 
  >>> ds1 = .... # X: some dataset, with whatever variable
  >>> ds2 = .... # Y: some dataset, same dimension as ds1

  >>> slope_linreg = cLinearRegression(ds1, ds2) # -> field of slope values for each grid points (between the time series of the corresponding grid points of X and Y)
  
  >>> ts1 = space_average(ds1)
  >>> slope_linreg2 = cLinearRegression(ts1, ds2) # -> field of slope values between the time series ts1 and the field ds2

**Side effects** : None

**Implementation** : need CDAT installed

