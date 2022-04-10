import math

class MatrixTransposition():
    def __init__(self):
        pass

    def encrypt(self,plainText,key):        
        plainText = plainText.replace(" ","%")

        col = len(key)
        row = math.ceil(len(plainText)/col)
        
        mat = [ [None]*col for i in range(row)]
        encrypted_text = []

        count = 0
        for i in range(row):
            for j in range(col):
                mat[i][j] = plainText[count]
                count+=1
                if count==len(plainText):
                    break
            else:
                continue
            break
        
        for i in range(col):
            cur_col= key[i] -1
            for j in range(row):
                if mat[j][cur_col]:
                    encrypted_text.append(mat[j][cur_col])

        return ''.join(encrypted_text)

    def decrypt(self,encrypted_text,key):

        col = len(key)
        row = math.ceil(len(encrypted_text)/col)
        
        mat = [ [None]*col for i in range(row)]
        decrypted_text = []
        count=0
        for i in range(col):
            cur_col = key[i]-1
            for j in range(row):
                if j==row-1 and len(encrypted_text) % col>0 and cur_col>=len(encrypted_text) % col:
                    continue
                mat[j][cur_col] = encrypted_text[count]
                count+=1
                if count>len(encrypted_text)-1:
                    break
            else:
                continue
            break
        li = [y if y else '' for x in mat for y in x]
        return ''.join(li).replace("%"," ")

if __name__=="__main__":
    mt = MatrixTransposition()

    input_text = "HELLO"
    
    with open('input/input2.txt') as f:
        input_text = f.read()
    
    print('\n'+"Input Text"+'\n')
    print(input_text+'\n')

    key= [5,4,1,3,2]

    encrypted_text = mt.encrypt(str(input_text),key)

    print('\n'+"Encrypted Text"+'\n')
    print(encrypted_text+'\n')
    print("Transformed text"+'\n')

    decrypted_text = mt.decrypt(encrypted_text,key)

    print(decrypted_text+'\n')

