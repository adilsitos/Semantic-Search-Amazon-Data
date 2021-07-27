MODEL_PATH =
TOKENIZER_PATH = 
NUMERICALIZE_PATH = 

fastai_model = torch.load(MODEL_PATH)
fastai_tok = torch.load(TOKENIZER_PATH)
fastai_num = toch.load(NUMERICALIZE_PATH)


class String2Emb:
	"Transform user input string into sentence embeddings using the encoder of a language model"
	def __init__(self, model, tokenizer, num):
		self.model = model
		self.model.eval()
		self.model.reset()
		self.numericalize = num
		self.tokenizer = tokenizer

	def str2emb(self, user_input):
		self.model.reset()
		tok_string = self.tokenizer(user_input)
		num_string = self.numericalize(tok_string)
		embeddings = model[0](num_string[None])[0]
		mean_embeddings = embeddings.mean(0)
		return mean_embeddings

