import math
from prettytable import PrettyTable

def main():
	table = PrettyTable()
	table.field_names = ["Rank","BM25 Value","File Name","File Number"]

	file1 = open('animal_list.txt','r')
	lines = file1.readlines()

	query = input("Enter the query: ")
	query = query.split(' ')
	query = [i.lower() for i in query]

	#Create a vocabulary for the query
	vocabulary = set()
	for token in query:
		vocabulary.add(token)
	vocab = list(vocabulary)

	N = 100
	ni = [0 for i in range(len(vocab))]

	#Calculating ni for each query term
	for i in range(len(vocab)):
		q = vocab[i]
		for line in lines:
			animal = line.strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			for j in range(len(text)):
				if(text[j]==q):
					ni[i]+=1
					break
	#Calculate Term-frequency factor Fij
	fij = [[0 for i in range(len(vocab))] for j in range(len(lines))]
	for i in range(len(vocab)):
		for j in range(len(lines)):
			word = vocab[i]
			animal = lines[j].strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			for k in range(len(text)):
				if(text[k]==word):
					fij[j][i]+=1

	#Calculate average document length
	avg_doclen = 0
	for line in lines:
		animal = line.strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		avg_doclen += len(text)

	avg_doclen /= N

	K1 = float(input("Enter the value of K1: "))
	b = float(input("Enter the value of b: "))

	#Calculate Bij
	Bij = [[0 for i in range(len(vocab))] for j in range(len(lines))]
	for i in range(len(vocab)):
		for j in range(len(lines)):
			animal = lines[j].strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			val = (1 - b) + ((b * len(text))/avg_doclen)
			Bij[j][i] = ((K1 + 1) * fij[j][i])/((K1 * val) + fij[j][i])

	#Calculate the value for BM25
	BM25 = [0 for i in range(N)]
	for k in range(len(lines)):
		animal = lines[k].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')

		for i in range(len(vocab)):
			q = vocab[i]
			for j in range(len(text)):
				if(text[j]==q):
					BM25[k] += Bij[k][i] * math.log2((N - ni[i] + 0.5)/(ni[i] + 0.5))
	#print(BM25)
	similarity = []
	for i in range(len(lines)):
		animal = lines[i].strip()
		similarity.append([BM25[i],animal,"D"+str(i+1)])

	similarity = sorted(similarity,reverse=True)

	i=1
	for k in range(len(lines)):
		animal = lines[k].strip()
		table.add_row([i,similarity[k][0],similarity[k][1],similarity[k][2]])
		i+=1

	print("Table of BM25 values wrt 100 Documents:")
	print(table)

if __name__ == '__main__':
	main()