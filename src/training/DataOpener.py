import pandas as pd


class DataOpener:

    def ReadFromCsv(self, filePathName):
        data = pd.read_csv(filePathName)
        return data

    def ReadFromExcel(self, filePathName):
        data = pd.read_excel(filePathName)
        return data

    def ReadFromJson(self, filePathName):
        data = pd.read_json(filePathName)
        return data
