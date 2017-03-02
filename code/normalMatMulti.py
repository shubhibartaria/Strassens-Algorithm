import sys
'''
This code multiplies the matrices in normal way and prints the answer
'''

def main():
	filename=input("Please enter the testcase input filename: ") #reading the filename
	readmat(filename) #opening file


'''def readmat(filename):
	#assuming format of input file to be the same as instructions in LabStressen.pdf
	with open(filename) as fh:
		while True:	
			x=fh.readline() 
			if (x==""): #if EOF
				break
			elif (x=="\n"): #if a newline, skip this line
				continue
			A=[] #matrix A
			B=[] #matrix B
			C=[]
			#if (fh.readline=="\n"):
			#	next(fh)
			n=int(x.strip()) #the size of the matrices
			for i in range(n):
				A.append([int(x) for x in fh.readline().split()]) #making matrix A using list comprehension
			for i in range(n):
				B.append([int(x) for x in fh.readline().split()]) #making array B
'''
def readmat(filename,fho):
	'''
	This method reads in the input file and calls the normal matrix multiplication algorithm on each
	set of matrices
	Given the input filename and the file handle for the output file, this calls the matrix multiplication 
	and prints the answer echoing the inputs
	'''
	#assuming format of input file to be the same as instructions in LabStressen.pdf
	try:
		with open(filename) as fh:
			while True:	
				x=fh.readline() 
				if (x==""): #if EOF
					break
				elif (x=="\n"): #if a newline, skip this line
					continue
				A=[] #matrix A
				B=[] #matrix B
				C=[]
				#if (fh.readline=="\n"):
				#	next(fh)
				try:
					n=int(x.strip()) #the size of the matrices
				except: #If the size of the matrix is not a number
					print("The size of the matrix is not a number. Try again")
					return
				try:
					for i in range(n):
						A.append([int(x) for x in fh.readline().split()]) #making matrix A using list comprehension
					for i in range(n):
						B.append([int(x) for x in fh.readline().split()]) #making array B
				except:
					print("The inputs are not of the correct format. Please modify into a proper format.")
					return
				try:
					assert n==len(A)
					assert n==len(B)
					for i in range(n):
						assert n==len(A[i])
						assert n==len(B[i])
				except:
					print("The size of the matrices are not equal to the input size. Modify and try again.")
					return

				C=matMultiply(A,B,n) #Calling the main Strassen algo with array A and B before moving on to the next 2 matrices
				print ("A = ",file=fho)
				printing(A,fho)
				print ("B = ",file=fho)
				printing(B,fho)
				print ("C = ",file=fho)
				printing(C,fho)
			#print ("A=\n",A,"\nB=\n",B,"\nC=\n",C,"\n\n")
	except:
		print("Unable to open the file. Please check the input file name or the location of the file.")
		return

def printing(A,fho):
	'''
	This method prints the matrices in proper format.
	Given the mattrix and output filehandle, this prints the matrix
	'''
	for i in range(len(A)):
		for j in range(len(A[i])):
			print (A[i][j], end=" ",file=fho)
		print(file=fho)
	print(file=fho)
	

def matMultiply(A,B,n):
	'''
	This method is the main method that contains code to execute normal matrix multiplication
	Given: The matrix A and B and the size of the matrices n, this returns the multiplied matrix
	C
	'''
	C=[[0 for x in range(n)] for y in range(n)]
	
	for i in range(n):
		for j in range(n):
			for k in range(n):
				
				C[i][j]+=(A[i][k]*B[k][j])
	return C

if __name__=="__main__":
	countmulti=0
	main()