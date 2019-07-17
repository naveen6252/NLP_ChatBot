import pandas as pd

if __name__ == '__main__':
	data = pd.read_csv('https://raw.githubusercontent.com/drazenz/heatmap/master/autos.clean.csv')
	corr = data.corr()
	print(corr)