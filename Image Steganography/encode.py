import cv2 # OpenCV 2

def to_bit_generator(msg):
    """Converts a message into a generator which returns 1 bit of the message
    each time."""
    for c in (msg):
        o = ord(c)
        for i in range(8):
            yield (o & (1 << i)) >> i

def main():
    # Create a generator for the hidden message
    hidden_message = to_bit_generator(open("encrypted_txt.txt", "r").read())
    print(hidden_message)
    # Read the original image
    bit = []
    count = 0
    for i in hidden_message:
        bit.append(i)
        count+=1
    k =0

    img = cv2.imread('pp.jpeg', cv2.IMREAD_GRAYSCALE)
    ##
    for h in range(len(img)):

        for w in range(len(img[0])):
            

            # Write the hidden message into the least significant bit
            if count > 0 :
                img[h][w] = (img[h][w] & ~1 | (bit[k]))
                count-=1
                k+=1
            else:
                img[h][w] = (img[h][w] & ~1 )
    cv2.imwrite("output1.png", img)

if __name__ == "__main__":
	main()
