import time
import pandas as pd

class Function:

    def TimeFunction(self,n):
        time.sleep(n)

    def DataLoad(self,csv):
        df = pd.read_csv(csv)
        return [csv,len(list(df))]

    def Binning(self,rulefile,csv):
        df = pd.read_csv(csv)
        


