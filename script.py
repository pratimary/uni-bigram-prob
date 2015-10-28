import operator
import collections
textfile= "NLP/input.txt"

Unigrams = {}
Bigrams = {}
count_bucket={}
count_bucket_bigram={}
unigram_counts={}
bigram_counts={}
GT_prob_unigram={}
GT_prob_bigram={}
all_tokens=[]
total_tokens=[]
all_bigrams=[]
total_count=0
total_bigram_count=0

prev_wrd='<START>'

for line in open(textfile):
	line=line.rstrip()
	tokens= line.split('\n')
	total_count=total_count + len(tokens)
	for word in tokens:
		#constructing unigram counts
		if word in Unigrams:
			Unigrams[word]+=1
			all_tokens.append(word)
		else:
			Unigrams[word]=1
			total_tokens.append(word)    #without repetition
			all_tokens.append(word)
		#constructing bigram counts
		bigram_word= prev_wrd+ ' '+ word
		
		if bigram_word in Bigrams:
			Bigrams[bigram_word]+=1
			total_bigram_count +=1
		else:
			if prev_wrd != '<START>':
				Bigrams[bigram_word]=1
				total_bigram_count +=1

		prev_wrd=word

#all possible bigrams
total_bigrams=0
for i in range(0,total_count):
	for j in range(0,total_count):
		all_bigram_words= all_tokens[i]+' '+all_tokens[j]
		if all_bigram_words not in all_bigrams:
			all_bigrams.append(all_bigram_words)
			total_bigrams+=1


print total_bigrams

total_tokens.sort(key=str.lower)
all_bigrams.sort(key=str.lower)

unigram_counts=dict(Unigrams)
bigram_counts=dict(Bigrams)

#print unigram_counts
#output unigram probabilities...
output_file = open('NLP/unigrams.txt','w')
for word in total_tokens:
	Unigrams[word]=float(Unigrams[word])/total_count
	#print "%s   %f"%(word,Unigrams[word])
	output_file.write("%-20s %-20s \n" % (word,str(Unigrams[word])))
output_file.close()

#print all_bigrams
#output bigrams prababilities
output_file=open('NLP/bigrams.txt','w')
for word in all_bigrams:
	tokens=word.split(" ")
	if tokens[0]:
		#print word
		denominator=unigram_counts[tokens[0]]
		if word in Bigrams:
			#print " count %s   %f"%(word,Bigrams[word])
			
			Bigrams[word]=float(Bigrams[word])/denominator
			#print "prob %s   %f"%(word,Bigrams[word])
			output_file.write(word+'\t\t'+str(Bigrams[word])+'\n')
		else:
			Bigrams[word]=0
			
			output_file.write("%-20s %-20s \n" % (word,str(Bigrams[word])))
output_file.close()


#creating bucket and good turing discounting- unigram

for word in unigram_counts:
	if unigram_counts[word] in count_bucket:
		count_bucket[unigram_counts[word]] +=1
	else:
		count_bucket[unigram_counts[word]] =1


output_file=open('NLP/unigrams_GT.txt','w')
for word in total_tokens:
	c=unigram_counts[word]
	cplus1=c+1
	if cplus1 in count_bucket:
		NCplus1=count_bucket[cplus1]
	else:
		NCplus1=0
	
	NC=count_bucket[c]
	
	
	cstar= cplus1 * NCplus1
	GT_prob_unigram[word]=(float(cstar)/NC)/total_count
	output_file.write("%-20s %-20s \n" % (word,str(GT_prob_unigram[word])))
output_file.close()

#creating bucket and good turing discounting- bigram
count_bucket_bigram[0]=0
for word in Bigrams:
	if word in bigram_counts:
		if bigram_counts[word] in count_bucket_bigram:
			count_bucket_bigram[bigram_counts[word]] +=1
		else:
			count_bucket_bigram[bigram_counts[word]] =1
	else:
		count_bucket_bigram[0]+=1

Bigrams = collections.OrderedDict(sorted(Bigrams.items()))
print count_bucket_bigram


output_file=open('NLP/bigrams_GT.txt','w')
for word in all_bigrams:
	if word in bigram_counts:
		c=bigram_counts[word]
	else:
		c=0
	cplus1=c+1
	if cplus1 in count_bucket_bigram:
		NCplus1=count_bucket_bigram[cplus1]
	else:
		NCplus1=0

	NC=count_bucket_bigram[c]
	cstar= cplus1 * NCplus1
	if c==0:
		GT_prob_bigram[word]=float(NCplus1)/total_bigram_count
	else:
		GT_prob_bigram[word]=(float(cstar)/NC)/total_bigram_count
	
	output_file.write("%-20s %-20s \n" % (word,str(GT_prob_bigram[word])))
output_file.close()

