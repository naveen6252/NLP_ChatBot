import custom_exceptions as exc
from settings import NLU_MODEL_PATH
from rasa_nlu.model import Interpreter
import pandas as pd
from datetime import datetime
from duckling import DucklingWrapper
from custom_exceptions import *
import numpy as np

duckling = DucklingWrapper()


# Function to fill aggregation in fact_condition
def fill_aggregation(raw_agg):
	df = pd.DataFrame(raw_agg)
	# if first is present then fill them down first
	if all(df.iloc[0].isna()):
		df = df.fillna(method='ffill').fillna(method='bfill')
	else:
		df = df.fillna(method='bfill').fillna(method='ffill')
	# default aggregate_function
	if 'aggregate_functions' not in df.columns:
		df['aggregate_functions'] = 'sum'
	raw_agg = df.to_dict('records')
	return raw_agg

def get_aggregation(entities, i):
	aggregation = {}
	if entities[i]['entity'] == 'agg':
		aggregation['aggregate_functions'] = entities[i]['value']
		i += 1
		ent = entities[i]['entity'] if i < len(entities) else 'NULL'
		if ent == 'fact':
			aggregation['facts'] = entities[i]['value']
			return aggregation, i
		else:
			return aggregation, i - 1
	if entities[i]['entity'] == 'fact':
		aggregation['facts'] = entities[i]['value']
		i += 1
		ent = entities[i]['entity'] if i < len(entities) else 'NULL'
		if ent == 'agg':
			aggregation['aggregate_functions'] = entities[i]['value']
			return aggregation, i
		else:
			return aggregation, i - 1
	else:
		raise NotImplementedError("get_aggregation should be used for agg and fact only")


def get_fact_condition_formatted(entities):
	fact_conditions = []
	i = 0
	while i < len(entities):
		if entities[i]['entity'] in ('agg', 'fact'):
			aggregation, i = get_aggregation(entities, i)
			fact_condition = {'aggregation': aggregation}
			i += 1
			ent = entities[i]['entity'] if i < len(entities) else 'NULL'
			val = entities[i]['value'] if i < len(entities) else 'NULL'
			if ent != 'fact_condition':
				i -= 1
			else:
				condition = val
				i += 1
				ent = entities[i]['entity'] if i < len(entities) else 'NULL'
				if ent in ('agg', 'fact'):
					aggregation, i = get_aggregation(entities, i)
					fact_condition['conditions'] = condition
					fact_condition['fact_value'] = aggregation
				elif ent == 'CARDINAL':
					fact_condition['conditions'] = condition
					fact_condition['fact_value'] = duckling.parse_number(entities[i]['value'])[0]['value']['value']
				else:
					i -= 1
			fact_conditions.append(fact_condition)
		elif entities[i]['entity'] == 'fact_condition':
			fact_condition = {}
			fact_condition['conditions'] = entities[i]['value']
			i += 1
			ent = entities[i]['entity'] if i < len(entities) else 'NULL'
			val = entities[i]['value'] if i < len(entities) else 'NULL'
			if ent == 'CARDINAL':
				fact_condition['fact_value'] = duckling.parse_number(val)[0]['value']['value']
			elif ent in ('agg', 'fact'):
				aggregation, i = get_aggregation(entities, i)
				fact_condition['fact_value'] = aggregation
			else:
				i -= 1
			fact_conditions.append(fact_condition)
		i += 1
	raw_fact_conditions = fact_conditions
	if not raw_fact_conditions:
		return {'aggregation': {'SalesAmount': ['sum']}, 'conditions': [{
			'fact_name': 'SalesAmount sum', 'conditions': np.nan, 'fact_value': np.nan}]}

	# try to fill aggregations in raw_fact_conditions
	df = pd.DataFrame(raw_fact_conditions)

	# No fact found and condition found, fact and its condition could not be bounded
	if 'aggregation' not in df.columns:
		raise NoFactError("Facts not found! or their conditions could not bounded")

	# default condition and fact_value
	if 'conditions' not in df.columns:
		df['conditions'] = np.nan
		df['fact_value'] = np.nan

	df['aggregation'] = df['aggregation'].fillna(method='ffill').fillna(method='bfill')
	raw_fact_conditions = df.to_dict('records')

	# try to fill aggregate_function and facts
	raw_agg = [agg['aggregation'] for agg in raw_fact_conditions]
	raw_agg = fill_aggregation(raw_agg)

	# raw_agg back to fact_conditions
	for i, fact_condition in enumerate(raw_fact_conditions):
		fact_condition['aggregation'] = raw_agg[i]

	facts = [cond['aggregation']['facts'] for cond in raw_fact_conditions] + [
		fact['fact_value']['facts'] if type(fact['fact_value']) == dict and 'facts' in fact['fact_value'] else np.nan
		for fact in raw_fact_conditions]

	# unique and drop na
	facts = [x for x in list(set(facts)) if x is not np.nan]

	aggregation = {fact: [] for fact in facts}
	conditions = []
	for i, cond in enumerate(raw_fact_conditions):
		if type(cond['fact_value']) == dict:
			if 'facts' not in cond['fact_value']:
				raise NoFactInOperand("Could not compare facts with multiple aggregations...")
			if 'aggregate_functions' not in cond['fact_value']:
				cond['fact_value']['aggregate_functions'] = cond['aggregation']['aggregate_functions']
			aggregation[cond['fact_value']['facts']].append(cond['fact_value']['aggregate_functions'])
			cond['fact_value'] = cond['fact_value']['facts'] + ' ' + cond['fact_value']['aggregate_functions']
		agg = cond['aggregation']
		dictionary = {'fact_name': agg['facts'] + ' ' + agg['aggregate_functions'], 'conditions': cond[
			'conditions'], 'fact_value': cond['fact_value']}
		if agg['aggregate_functions'] not in aggregation[agg['facts']]:
			aggregation[agg['facts']].append(agg['aggregate_functions'])
		if dictionary not in conditions:
			conditions.append(dictionary)

	return {'aggregation': aggregation, 'conditions': conditions}



if __name__ == '__main__':
	interpreter = Interpreter.load(NLU_MODEL_PATH)
	query = input("Enter query(/stop to stop):\n->")
	while query != '/stop':
		entities = interpreter.parse(query)
		entities = entities['entities']
		# Sort Entities by their end position in the query
		entities_df = pd.DataFrame(entities).sort_values('end', ascending=True)
		entities = list(entities_df.T.to_dict().values())
		fact_condition = get_fact_condition_formatted(entities)
		print(fact_condition)
		query = input("Enter query(/stop to stop):\n->")

		a = [
			{'entity': 'DATE', 'value': 'last month', 'start': 18, 'confidence': None, 'end': 28,
			 'extractor': 'SpacyEntityExtractor'},
			{'start': 8, 'end': 13, 'value': 'SalesAmount', 'entity': 'fact', 'confidence': 0.9961891327557518,
			 'extractor': 'CRFEntityExtractor', 'processors': ['EntitySynonymMapper']},
			{'start': 14, 'end': 17, 'value': 'equal_to', 'entity': 'date_condition', 'confidence': 0.9919232241736908,
			 'extractor': 'CRFEntityExtractor', 'processors': ['EntitySynonymMapper']},
			{'start': 18, 'end': 28, 'text': 'last month', 'value': '2019-05-01T00:00:00.000-07:00', 'confidence': 1.0,
			 'additional_info': {
				 'values': [{'value': '2019-05-01T00:00:00.000-07:00', 'grain': 'month', 'type': 'value'}],
				 'value': '2019-05-01T00:00:00.000-07:00', 'grain': 'month', 'type': 'value'},
			 'entity': 'time',
			 'extractor': 'DucklingHTTPExtractor'}
		]

		b = [
			{'entity': 'DATE', 'value': 'last month', 'start': 20, 'confidence': None, 'end': 30,
			 'extractor': 'SpacyEntityExtractor'},
			{'start': 8, 'end': 13, 'value': 'SalesAmount', 'entity': 'fact', 'confidence': 0.9920408957694943,
			 'extractor': 'CRFEntityExtractor', 'processors': ['EntitySynonymMapper']},
			{'start': 14, 'end': 19, 'value': 'greater_than', 'entity': 'date_condition',
			 'confidence': 0.9924836442452525, 'extractor': 'CRFEntityExtractor',
			 'processors': ['EntitySynonymMapper']},
			{'start': 14, 'end': 30, 'text': 'after last month',
			 'value': {'to': None, 'from': '2019-05-01T00:00:00.000-07:00'}, 'confidence': 1.0,
			 'additional_info': {
				 'values': [
					 {'from': {'value': '2019-05-01T00:00:00.000-07:00', 'grain': 'month'}, 'type': 'interval'}
				 ], 'from': {'value': '2019-05-01T00:00:00.000-07:00', 'grain': 'month'},
				 'type': 'interval'},
			 'entity': 'time', 'extractor': 'DucklingHTTPExtractor'}]

		c = [{'entity': 'DATE', 'value': 'last 1 month', 'start': 18, 'confidence': None, 'end': 30,
			  'extractor': 'SpacyEntityExtractor'},
			 {'start': 8, 'end': 13, 'value': 'SalesAmount', 'entity': 'fact', 'confidence': 0.9961891048907205,
			  'extractor': 'CRFEntityExtractor', 'processors': ['EntitySynonymMapper']},
			 {'start': 14, 'end': 17, 'value': 'equal_to', 'entity': 'date_condition', 'confidence': 0.9919223810305202,
			  'extractor': 'CRFEntityExtractor', 'processors': ['EntitySynonymMapper']},
			 {'start': 18, 'end': 30, 'text': 'last 1 month',
			  'value': {'to': '2019-06-01T00:00:00.000-07:00', 'from': '2019-05-01T00:00:00.000-07:00'},
			  'confidence': 1.0, 'additional_info': {'values': [
				 {'to': {'value': '2019-06-01T00:00:00.000-07:00', 'grain': 'month'},
				  'from': {'value': '2019-05-01T00:00:00.000-07:00', 'grain': 'month'}, 'type': 'interval'}],
				 'to': {'value': '2019-06-01T00:00:00.000-07:00', 'grain': 'month'},
				 'from': {'value': '2019-05-01T00:00:00.000-07:00',
						  'grain': 'month'}, 'type': 'interval'}, 'entity': 'time',
			  'extractor': 'DucklingHTTPExtractor'}]


