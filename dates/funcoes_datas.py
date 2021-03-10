
# gera uma lista com os anomes
def rangemes(i, j):
	r=[]
	while i <= j:
		r.append(i)
		if i%100<12:
			i+=1
		else:
			i+=89
	return r




