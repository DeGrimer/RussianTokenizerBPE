import regex as re
from base import get_stats, merge, render_token, Tokenizer
from tqdm import tqdm
def main():
	with open('E:\\lurk\\output.txt', 'r',encoding='utf-8') as r:
	    text = r.read()
	testText = text
	vocab_size = 1024
	tokenizer = Tokenizer()
	tokenizer.register_special_tokens({"<|endoftext|>": 100257})
	tokenizer.train(testText, vocab_size)
	tokenizer.save("RusTokenModel")
if __name__ == "__main__":
	main()