import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn')
from orbit.models.dlt import ETSFull


class OrbitETS(ETSFull):

    def __init__(self, date_col, response_col, **kwargs):
        super().__init__(date_col=date_col, response_col=response_col, **kwargs)
        self.name = 'OrbitETS'
        self.__prediction = None
        self.__test = None

    def fit(self, train):
        new_train = train.copy()
        new_train[self.date_col] = pd.to_numeric(new_train[self.date_col])

        super(OrbitETS, self).fit(df=new_train)

    def predict(self, test, **kwargs):
        new_test = test.copy()
        new_test[self.date_col] = pd.to_numeric(new_test[self.date_col])

        prediction = super(OrbitETS, self).predict(new_test)

        prediction[self.date_col] = pd.to_datetime(prediction[self.date_col])
        prediction = prediction[['time', 'prediction']]
        prediction.columns = ['time', 'price']

        return prediction

    def show(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.__test['time'], self.__test['price'], c='b', label="real")
        ax.plot(self.__test['time'], self.__prediction['price'], c='r', label="prediction")
        plt.legend()
        plt.show()
