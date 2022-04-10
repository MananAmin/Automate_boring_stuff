import re

# Ignore spaces, punctuations, and line breaks.
class playfair():
    def __init__(self,key):
        self.key = key.replace("J","I")
        self.mat = [ [0]*5 for i in range(5)]
        self.__create_matrics()

    def __create_matrics(self):
        if self.key:
            visited = set()
            key_len = len(self.key)
            cur = len(self.key)
            cur_alpha = "A"
            for i in range(5):
                for j in range(5):
                    if cur>1:
                        while self.key[key_len-cur] in visited and cur>1:
                            cur-=1
                        if cur>1:
                            self.mat[i][j] = self.key[key_len-cur]
                            visited.add(self.key[key_len-cur])

                            if self.key[key_len-cur] == "I":
                                visited.add("I")
                                visited.add("J")
                            cur-=1
                            continue
            
                    while cur_alpha in visited:
                        cur_alpha = chr(ord(cur_alpha)+1)
                    self.mat[i][j] = cur_alpha
                    if cur_alpha == "I" or cur_alpha == "J":
                        visited.add("I")
                        visited.add("J")
                    visited.add(cur_alpha)
                        
    
    def print_matrics(self):
        print(self.mat)

    def set_key(self,key) -> None:
        self.key = key.replace("J","I")
        self.__create_matrics()

    def create_dict(self):
        temp = {}
        for i in range(5):
            for j in range(5):
                temp[self.mat[i][j]] = [i,j]
        return temp

    # Encrpy 2 char using dict
    def encrypt_ch(self,pt,mat_dict):
        if len(pt)!=2:
            return ""
        r1,c1 = mat_dict[pt[0]]
        r2,c2 = mat_dict[pt[1]]
        if r1==r2:
            return self.mat[r1][(c1+1)%5] + self.mat[r2][(c2+1)%5]
        elif c1==c2:
            return self.mat[(r1+1)%5][c1] + self.mat[(r2+1)%5][c2]
        return self.mat[r1][c2] + self.mat[r2][c1]

    def encrypt(self,plainText):

        # Removing spaces, punctuations, and line breaks.
        pattern = re.compile(r'[^a-zA-Z]+')
        plainText = re.sub(pattern, '', plainText)
        plainText = plainText.upper().replace("J","I")

        # creating dict for fast lookup 
        mat_dict = self.create_dict() 

        encrypted_text = []
        last_ch = ""
        cur = ""
        flag = False
        special_encrypt = "X"

        for ch in plainText:
            # same char case
            if flag and last_ch==ch:
                cur = last_ch+special_encrypt
                encrypted_text.append(self.encrypt_ch(cur,mat_dict))

            # different char
            elif flag:
                cur=last_ch+ch
                encrypted_text.append(self.encrypt_ch(cur,mat_dict))
                flag=False

            # odd char case
            else:
                cur = ch
                flag = True
                last_ch=ch

        # case for odd numbers of chars, padded Z
        if len(cur)==1:
            encrypted_text.append(self.encrypt_ch(cur+"Z",mat_dict))

        return ''.join(encrypted_text)

    def decrypt_char(self,e1,e2,mat_dict):
        r1,c1 = mat_dict[e1]
        r2,c2 = mat_dict[e2]
        if r1==r2:
            return self.mat[r1][(c1-1)%5] + self.mat[r2][(c2-1)%5]
        elif c1==c2:
            return self.mat[(r1-1)%5][c1] + self.mat[(r2-1)%5][c2]
        return self.mat[r1][c2] + self.mat[r2][c1]


    def decrypt(self,encrypted_text):
        # Removing spaces, punctuations, and line breaks.
        pattern = re.compile(r'[^a-zA-Z]+')
        encrypted_text = re.sub(pattern, '', encrypted_text)
        encrypted_text = encrypted_text.upper()

        # creating dict for fast lookup 
        mat_dict = self.create_dict() 

        decrypted_text = []
        for i in range(len(encrypted_text)//2):
            decrypted_text.append(self.decrypt_char(encrypted_text[i*2],encrypted_text[i*2+1],mat_dict))

        return ''.join(decrypted_text)

if __name__=="__main__":
    pf = playfair("RAYQUAZA")
    pf.print_matrics()
    input_text = "HELLO"
    
    with open('input/input1.txt') as f:
        input_text = f.read()

    encrypted_text = pf.encrypt(str(input_text))

    print('\n'+"Encrypted Text"+'\n')
    print(encrypted_text+'\n')
    print("Transformed text"+'\n')

    decrypted_text = pf.decrypt(encrypted_text)

    print(decrypted_text+'\n')