# Ref: https://crypto.stackexchange.com/questions/13166/method-to-calculating-e-in-rsa
# Ref: https://gist.github.com/tylerl/1239116/8d9d75de90a37112be665a2aa1478eabfbdd6087
# Assignment 5

class RSA:
    def __init__(self, p,q) -> None:
        self.p = p
        self.q = q
        self.pub_keys,self.pvt_keys = self.__generate_keys()
    
    def print_keys(self):
        print("Public RSA key is :", self.pub_keys)
        print("Private RSA key is :", self.pvt_keys)

    def is_prime(self,num):
        if num%2==0 and num>2: return False
        i=3; sqrt=num**0.5
        while i<=sqrt:
            if num%i==0: return False
            i+=2
        return True

    def __generate_keys(self):
        print("Calculating RSA values..")
        n = self.p * self.q
        mul = (self.p-1)*(self.q-1)
        e =None
        temp = max(self.p,self.q) +1
        while not self.is_prime(temp):
            temp+=1
        e= temp
        d = self.mod_inverse(e,mul)
        # print(e," e d ",d)
        return ([e,n],[d,n])
    
    # basically this function calculate modular inverse using extended euclidian method
    # Ref: https://gist.github.com/tylerl/1239116/8d9d75de90a37112be665a2aa1478eabfbdd6087
    def mod_inverse(self,x,y):
        def eea(a,b):
            if b==0:return (1,0)
            (q,r) = (a//b,a%b)
            (s,t) = eea(b,r)
            return (t, s-(q*t) )
        inv = eea(x,y)[0]
        if inv < 1: inv += y
        return inv
    
    def pow(self,x,y):
        result=1
        p = x
        while y>0:
            if y%2==1:
                result= result*p
            y = y//2
            p = p*p
        return result

    def powmod(self,x,y,mod):
            result=1
            p = x%mod
            while y>0:
                if y%2==1:
                    result= (result*p)%mod
                y = y//2
                p = (p*p)%mod
            return result

    def encrypt(self,msg):
        if msg >=self.p* self.q:
            raise Exception("Number should be less than p*q")
        return self.powmod(msg,self.pub_keys[0],self.pub_keys[1])
    
    def decrpt(self,ct):
        return self.powmod(ct,self.pvt_keys[0],self.pvt_keys[1])

if __name__=="__main__":
    # User should enter valid prime otherwise it will result in bed algorithm
    print("Enter the prime numbers, ")
    p = int(input("p: "))
    q = int(input("q:"))

    rsa = RSA(p,q)
    rsa.print_keys()
    msg = int(input("Enter the plaintext message m (an integer): "))

    print("Encrypting m…")
    c =rsa.encrypt(msg)
    print("The ciphertext c is ",c)

    print("Decrypting c …")
    pt = rsa.decrpt(c)
    print("The plaintext m is ",pt)