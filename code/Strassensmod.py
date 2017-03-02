import sys
import normalMatMulti
import Strassens

'''
This program will execute the Strassens Algorithm for Matrix Multiplication with 2 approaches: one with
leaf size=1 and the other will leaf size=2. The methods for this are in the class Strassenexec.
It also uses the normal matrix multiplication method to compare
'''
def main():
	'''
	This main file executes the correct type of matrix multiplication depending upon the inputs
	Given the input filename and the output filename along with the choices, it calls the
	appropriate methods
	'''
	filename=input("Please enter the testcase input filename: ") #reading the filename
	outputfile=input("Please enter the output filename to which you want to append the answers to: ")
	fho=open(outputfile,'a')
	while True:
		choice=input("Select the leaf-size that you want: 1 or 2: ")
		if choice=="1":
			print("Strassens with leaf-size=1:", file=fho)
			readmat(filename,fho) #opening file
			break
		elif choice=="2":
			print("Strassens with leaf-size=2:", file=fho)
			Strassens.readmat(filename,fho)
			break
		else:
			print("Enter the correct choice. Try again!")
	
	choice=input("Do you want to execute the normal matrix multiplication method? 1:Yes 0:No : ")
	if choice=="1":
		print("The normal matrix multiplication method:", file=fho)
		normalMatMulti.readmat(filename,fho)
	elif choice=="0":
		print("Thank you!")
		return
	else:
		print("Wrong input. Bbye!")
		return

	


def readmat(filename,fho):
	'''
	This method reads in the input file and calls the Strassen's algorithm on each set of matrices
	Given the input filename and the file handle for the output file, this calls the Strassens algo 
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
					print("The inputs are not of the correct format. It may not be a number. Please modify into a proper format.")
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
				
				C=Strassenexec.Strassen(A,B,n) #Calling the main Strassen algo with array A and B before moving on to the next 2 matrices
				print ("A = ", file=fho)
				printing(A,fho)
				print ("B = ", file=fho)
				printing(B,fho)
				print ("C = ", file=fho)
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

class Strassenexec:
	'''
	This class is the main class that contains all methods to execute the Strassens algo
	'''
	def Strassen(A,B,n):
		'''
		This method is the main method that contains code to execute Strassens algo.
		Given: The matrix A and B and the size of the matrices n, this returns the multiplied matrix
		C
		'''

		if (n==1):
			return (Strassenexec.matMultiply(A,B,n))
		else:
			newn=int(n/2) #dividing the matrix n into n/2
		
			#initialising and dividing the matrix A and B into submatrices of size n/2 
			a11=[[0 for i in range(newn)] for j in range(newn)]
			a12=[[0 for i in range(newn)] for j in range(newn)]
			a21=[[0 for i in range(newn)] for j in range(newn)]
			a22=[[0 for i in range(newn)] for j in range(newn)]

			b11=[[0 for i in range(newn)] for j in range(newn)]
			b12=[[0 for i in range(newn)] for j in range(newn)]
			b21=[[0 for i in range(newn)] for j in range(newn)]
			b22=[[0 for i in range(newn)] for j in range(newn)]

			#dividing A and B into submatrices initialised above:
			for i in range(newn):
				for j in range(newn): #adding the appropriate offsets to create submatrices
					a11[i][j]=A[i][j]
					a12[i][j]=A[i][j+newn]
					a21[i][j]=A[i+newn][j]
					a22[i][j]=A[i+newn][j+newn]

					b11[i][j]=B[i][j]
					b12[i][j]=B[i][j+newn]
					b21[i][j]=B[i+newn][j]
					b22[i][j]=B[i+newn][j+newn]

			#satemp and sbtemp are different S1, S2, S3...S10 matrices that are being reused
			satemp=[[0 for i in range(newn)] for j in range(newn)]
			sbtemp=[[0 for i in range(newn)] for j in range(newn)]

			#To calculate P1 -> a11*(b12-b22)
			sbtemp=Strassenexec.subMat(b12,b22, newn)
			p1=Strassenexec.Strassen(a11,sbtemp,newn)
			#print ("p1=",p1)
		

			#p2=(a11+a12)*b22
			satemp=Strassenexec.addMat(a11, a12, newn)
			p2=Strassenexec.Strassen(satemp, b22, newn)
			#print ("p2=",p2)

			#p3=(a21+a22)*b11
			satemp=Strassenexec.addMat(a21, a22, newn)
			p3=Strassenexec.Strassen(satemp, b11, newn)
			#print ("p3=",p3)

			#p4=a22*(b21-b11)
			sbtemp=Strassenexec.subMat(b21,b11,newn)
			p4=Strassenexec.Strassen(a22, sbtemp, newn)
			#print ("p4=",p4)

			#p5=(a11+a22)*(b11+b22)
			satemp=Strassenexec.addMat(a11, a22, newn)
			sbtemp=Strassenexec.addMat(b11, b22, newn)
			p5=Strassenexec.Strassen(satemp, sbtemp, newn)
			#print ("p5=",p5)

			#p6=(a12-a22)*(b21+b22)
			satemp=Strassenexec.subMat(a12, a22, newn)
			sbtemp=Strassenexec.addMat(b21, b22, newn)
			p6=Strassenexec.Strassen(satemp, sbtemp, newn)
			#print ("p6=",p6)

			#p7=(a11-a21)*(b11+b12)
			satemp=Strassenexec.subMat(a11, a21, newn)
			sbtemp=Strassenexec.addMat(b11, b12, newn)
			p7=Strassenexec.Strassen(satemp, sbtemp, newn)
			#print ("p7=",p7)

			#Calculating the matrix C elements based on the p1..p7 values and reusing add and sub methods

			if (type(p1)!=int): #when the size of n is not 1, it returns a list, else it returns an int. Have to process it differently
				c12=Strassenexec.addMat(p1, p2, newn)
		
				c21=Strassenexec.addMat(p3, p4, newn)

				temp1=Strassenexec.addMat(p5, p4, newn)
				temp2=Strassenexec.subMat(temp1, p2, newn)
				c11=Strassenexec.addMat(temp2, p6, newn)

				temp1=Strassenexec.addMat(p5, p1, newn)
				temp2=Strassenexec.subMat(temp1, p3, newn)
				c22=Strassenexec.subMat(temp2, p7, newn)

				#Consolidating C
				C=[[0 for i in range(n)] for j in range(n)]

				for i in range(newn):
					for j in range(newn):
						C[i][j]=c11[i][j]
						C[i][j+newn]=c12[i][j]
						C[i+newn][j]=c21[i][j]
						C[i+newn][j+newn]=c22[i][j]

			else: #when size of n=1, sub and add returns int and not list. Have to process it differently
				c12=p1+p2

				c21=p3+p4

				c11=p5+p4-p2+p6

				c22=p5+p1-p3-p7

				#Consolidating C
				C=[[0 for i in range(n)] for j in range(n)]

				for i in range(newn):
					for j in range(newn):
						C[i][j]=c11
						C[i][j+newn]=c12
						C[i+newn][j]=c21
						C[i+newn][j+newn]=c22

		return C


	def addMat(A,B,n):
		'''
		This method contains code to execute matrix addition.
		Given: The matrix A and B and the size of the matrices n, this returns the added matrix
		C
		'''
		C=[[0 for x in range(n)] for y in range(n)]
		for i in range(n):
			for j in range(n):
				C[i][j]=(A[i][j]+B[i][j])
		return C

	def subMat(A,B,n):
		'''
		This method contains code to execute matrix subtraction.
		Given: The matrix A and B and the size of the matrices n, this returns the subtracted matrix
		C
		'''
		C=[[0 for x in range(n)] for y in range(n)]
		for i in range(n):
			for j in range(n):
				C[i][j]=(A[i][j]-B[i][j])
		return C

	def matMultiply(A,B,n): #we kept the size of n=1
		return (A[0][0]*B[0][0])


'''def matMultiply(A,B,n):
	C=[[0 for x in range(n)] for y in range(n)]
	for i in range(n):
		for j in range(n):
			for k in range(n):
				C[i][j]+=(A[i][k]*B[k][j])
	return C'''



			

if __name__=="__main__":
	main()