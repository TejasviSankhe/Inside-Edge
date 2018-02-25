"""Main script for generating output.csv."""
import pandas as pd 
import numpy as np 

def stat_avg(df):
    return (df['H'] / df['AB']).round(3)
    
def stat_obp(df):
    return ((df['H'] + df['BB'] + df['HBP']) / (df['AB'] + df['BB'] + df['HBP'] + df['SF'])).round(3)

def stat_slg(df):
    return (df['TB'] / df['AB']).round(3)

def stat_ops(df):
    return stat_obp(df) + stat_slg(df)

vs_Map = {'vs RHP': lambda df : df[df['PitcherSide'] == 'R'],
		'vs LHP': lambda df : df[df['PitcherSide'] == 'L'],
		'vs RHH': lambda df : df[df['HitterSide'] == 'R'],
		'vs LHH': lambda df : df[df['HitterSide'] == 'L'] }

def query_process(df, query):
	q = query.strip().split(',')

	#get split data
	sums = vs_Map[q[2]](df).groupby(q[1]).sum()
	q_df = sums[sums.PA >=25]


	if q[0] == 'AVG':
		value = pd.Series(stat_avg(q_df))
	elif q[0] == 'OBP':
		value = pd.Series(stat_obp(q_df))
	elif q[0] == 'SLG':
		value = pd.Series(stat_slg(q_df))
	else:
		value = pd.Series(stat_ops(q_df))

	ret = pd.DataFrame({'SubjectId' : q_df.index, 'Stat' : q[0], 'Subject' : q[1], 'Split' : q[2], 'Value' : value},columns=['SubjectId', 'Stat', 'Split', 'Subject', 'Value'])
	return ret




def main():
    # add basic program logic here
    pitch_data = pd.read_csv('./data/raw/pitchdata.csv')
    queries = open('./data/reference/combinations.txt').readlines()[1:]

    output = pd.DataFrame(columns=['SubjectId', 'Stat', 'Split', 'Subject', 'Value'])
    for q in queries:
    	temp = query_process(pitch_data, q)
    	output.append(temp)

    
    # sort and write to csv
    output.sort_values(by = ['SubjectId', 'Stat', 'Split', 'Subject'])
    output.to_csv('./data/processed/output.csv',index = False)

  


if __name__ == '__main__':
    main()
