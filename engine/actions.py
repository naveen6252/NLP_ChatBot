from rasa_core_sdk import Action


class ActionDimKPITableAdject(Action):
	def name(self):
		return "action_dim.kpi_table.adject"

	def run(self, dispatcher, tracker, domain):
		# cuisine = tracker.get_slot('cuisine')
		# q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
		dispatcher.utter_message('The action is action_dim.kpi_table.adject')
		return []
	# return [SlotSet("matches", ['action_dim.kpi.adject'])]


class ActionFactKPIDimFilter(Action):
	def name(self):
		return "action_fact.kpi.dim.filter"

	def run(self, dispatcher, tracker, domain):
		# cuisine = tracker.get_slot('cuisine')
		# q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
		dispatcher.utter_message('The action is action_fact.kpi.dim.filter')
		return []
	# return [SlotSet("matches", ['action_fact.kpi.dim.filter'])]


class ActionFactKPISingle(Action):
	def name(self):
		return "action_fact.kpi.single"

	def run(self, dispatcher, tracker, domain):
		# cuisine = tracker.get_slot('cuisine')
		# q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
		dispatcher.utter_message('The action is action_fact.kpi.single')
		return []
	# return [SlotSet("matches", ["action_fact.kpi.single"])]


class ActionFactTableGroup(Action):
	def name(self):
		return "action_fact.table.group"

	def run(self, dispatcher, tracker, domain):
		# cuisine = tracker.get_slot('cuisine')
		# q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)

		dispatcher.utter_message('The action is action_fact.table.group')
		return []
	# return [SlotSet("matches", ["action_fact.table.group"])]
