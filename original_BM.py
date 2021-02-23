import math
from prettytable import PrettyTable

def main():
	table = PrettyTable()
	table.field_names = ["Rank","BM15 Value","File Name","File Number"]

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

	#Finding the value of BM1
	BM1 = [0 for i in range(N)]
	for k in range(len(lines)):
		animal = lines[k].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')

		for i in range(len(vocab)):
			q = vocab[i]
			for j in range(len(text)):
				if(text[j]==q):
					BM1[k] += math.log2((N - ni[i] + 0.5)/(ni[i] + 0.5))
					break
	# print(BM1)
	
	#Steps for BM11 and BM15
	#Step 1: Term-frequency factor Fij
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

	K1 = float(input("Enter the value of K1: "))
	S1 = K1 + 1
	Fij = [[0 for i in range(len(vocab))] for j in range(len(lines))]
	for i in range(len(vocab)):
		for j in range(len(lines)):
			Fij[j][i] = S1 * (fij[j][i]/(K1 + fij[j][i]))

	#Step 2: Document length normalization Fij'
	#Calculate average document length
	avg_doclen = 0
	for line in lines:
		animal = line.strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		avg_doclen += len(text)

	avg_doclen /= N
	# print(avg_doclen)

	Fij_dash = [[0 for i in range(len(vocab))] for j in range(len(lines))]
	for i in range(len(vocab)):
		for j in range(len(lines)):
			animal = lines[j].strip()
			f1 = open(f'preprocessed_data/{animal}.txt','r')
			text = f1.read().split(' ')
			val = (K1 * len(text)) / avg_doclen
			if fij[j][i] > 0:
				Fij_dash[j][i] = S1 * (fij[j][i] / (val * fij[j][i]))

	#Step 3: Correction factor Gij
	K2 = float(input("Enter the value of K2: "))
	Gjq = [0 for j in range(len(lines))]
	for j in range(len(lines)):
		animal = lines[j].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		Gjq[j] = K2 * len(query) * ((avg_doclen - len(text))/(avg_doclen + len(text)))

	#Step 4: Term frequencies within queries
	K3 = float(input("Enter the value of K3: "))
	S3 = K3 + 1
	fiq = [0 for i in range(len(vocab))]
	for i in range(len(vocab)):
		for j in range(len(query)):
			word = vocab[i]
			if(query[j]==word):
				fiq[i]+=1

	Fiq = [0 for i in range(len(vocab))]
	for i in range(len(vocab)):
		Fiq[i] = S3 * (fiq[i]/(K3 + fiq[i]))

	#Calculate the value for BM15
	BM15 = [0 for i in range(N)]
	for k in range(len(lines)):
		animal = lines[k].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')

		BM15[k] += Gjq[k]
		for i in range(len(vocab)):
			q = vocab[i]
			for j in range(len(text)):
				if(text[j]==q):
					BM15[k] += Fij[k][i] * Fiq[i] * math.log2((N - ni[i] + 0.5)/(ni[i] + 0.5))
					break
	# print("BM15: ",BM15)

	#Calculate the value for BM11
	BM11 = [0 for i in range(N)]
	for k in range(len(lines)):
		animal = lines[k].strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')

		BM11[k] += Gjq[k]
		for i in range(len(vocab)):
			q = vocab[i]
			for j in range(len(text)):
				if(text[j]==q):
					BM11[k] += Fij_dash[k][i] * Fiq[i] * math.log2((N - ni[i] + 0.5)/(ni[i] + 0.5))
					break
	# print("BM11: ",BM11)
	similarity = []
	for i in range(len(lines)):
		animal = lines[i].strip()
		similarity.append([BM15[i],animal,"D"+str(i+1)])

	similarity = sorted(similarity,reverse=True)

	i=1
	for k in range(len(lines)):
		animal = lines[k].strip()
		table.add_row([i,similarity[k][0],similarity[k][1],similarity[k][2]])
		i+=1

	print("Table of BM values wrt 100 Documents:")
	print(table)

if __name__=='__main__':
	main()


