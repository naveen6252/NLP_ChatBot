from chatbot import entity_helpers
from settings import MAIN_NLU_DATA_PATH

if __name__ == '__main__':
	nlu_data = entity_helpers.read_nlu_data(MAIN_NLU_DATA_PATH)
	print(nlu_data)