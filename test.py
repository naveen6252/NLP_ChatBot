def convert_text_md_format(text, entities):
	length_to_add = 0
	for entity in entities:
		if entity['entity'] not in ['DATE', 'time', 'CARDINAL']:
			start = entity['start'] + length_to_add
			end = entity['end'] + length_to_add
			value = entity['value']
			ent = entity['entity']
			val_ent = ent + ":" + value
			prev = text[start:end]
			new = "[" + prev + "]" + "(" + val_ent + ")"
			text = text[:start] + new + text[end :]
			length_to_add += len(new) - len(prev)
	return text


if __name__ == '__main__':
	a = {'intent': {'name': 'fact.table.group', 'confidence': 0.5746628321163304},
		 'entities': [{'entity': 'CARDINAL',
					   'value': '5',
					   'start': 4,
					   'confidence': None,
					   'end': 5,
					   'extractor': 'SpacyEntityExtractor'},
					  {'entity': 'DATE',
					   'value': '2015 to 2018',
					   'start': 37,
					   'confidence': None,
					   'end': 49,
					   'extractor': 'SpacyEntityExtractor'},
					  {'start': 0,
					   'end': 3,
					   'value': 'top',
					   'entity': 'selection',
					   'confidence': 0.7690855970890293,
					   'extractor': 'CRFEntityExtractor'},
					  {'start': 6,
					   'end': 15,
					   'value': 'CustomerName',
					   'entity': 'dim',
					   'confidence': 0.5300859536166445,
					   'extractor': 'CRFEntityExtractor',
					   'processors': ['EntitySynonymMapper']},
					  {'start': 19,
					   'end': 24,
					   'value': 'North',
					   'entity': 'CustomerRegion',
					   'confidence': 0.9945166774653639,
					   'extractor': 'CRFEntityExtractor',
					   'processors': ['EntitySynonymMapper']},
					  {'start': 32,
					   'end': 36,
					   'value': 'greater_than',
					   'entity': 'date_condition',
					   'confidence': 0.985524392116838,
					   'extractor': 'CRFEntityExtractor',
					   'processors': ['EntitySynonymMapper']},
					  {'start': 42,
					   'end': 44,
					   'value': 'lesser_than',
					   'entity': 'date_condition',
					   'confidence': 0.9725409224398391,
					   'extractor': 'CRFEntityExtractor',
					   'processors': ['EntitySynonymMapper']},
					  {'start': 32,
					   'end': 49,
					   'text': 'from 2015 to 2018',
					   'value': {'to': '2019-01-01T00:00:00.000+05:30',
								 'from': '2015-01-01T00:00:00.000+05:30'},
					   'confidence': 1.0,
					   'additional_info': {'values': [{'to': {'value': '2019-01-01T00:00:00.000+05:30',
															  'grain': 'year'},
													   'from': {'value': '2015-01-01T00:00:00.000+05:30',
																'grain': 'year'},
													   'type': 'interval'}],
										   'to': {'value': '2019-01-01T00:00:00.000+05:30', 'grain': 'year'},
										   'from': {'value': '2015-01-01T00:00:00.000+05:30', 'grain': 'year'},
										   'type': 'interval'},
					   'entity': 'time',
					   'extractor': 'DucklingHTTPExtractor'}],
		 'intent_ranking': [{'name': 'fact.table.group',
							 'confidence': 0.5746628321163304},
							{'name': 'fact.kpi', 'confidence': 0.11345194634317686},
							{'name': 'agent.origin', 'confidence': 0.01602336735885628},
							{'name': 'fact.table.logic', 'confidence': 0.014866839945263792},
							{'name': 'agent.be_clever', 'confidence': 0.01412637355638571},
							{'name': 'user.will_be_back', 'confidence': 0.01297349571936961},
							{'name': 'greetings.goodmorning', 'confidence': 0.01050477085125581},
							{'name': 'greetings.whatsup', 'confidence': 0.010072776417815186},
							{'name': 'greetings.bye', 'confidence': 0.008981370763931434},
							{'name': 'agent.age', 'confidence': 0.00842825298878433}],
		 'text': 'top 5 customers in north region from 2015 to 2018'}

	convert_text_md_format(a['text'], a['entities'])

	'[top](selection:top) 5 [customers](dim:CustomerName) in [north](CustomerRegion:North) region [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018'