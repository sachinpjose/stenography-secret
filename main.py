# Import libraries
import sys
import cv2
import numpy as np


def convert_to_binary(message):
    if isinstance(message, str):
        # "sample" --> output as a list --> ['01110011', '01100001', '01101101', '01110000', '01101100', '01100101']
        #  List is joined to a string of binary '011100110110000101101101011100000110110001100101'
        #  Ord(i) --> converts string to ASCII
        #  Format of 08b --> returns a 8 bit
        return "".join([format(ord(i), "08b") for i in message])

    elif type(message) in [bytes, np.ndarray]:
        return [format(i, "08b") for i in message]

    elif type(message) in [int, np.uint8]:
        return format(message, "08b")

    else:
        print("Unsupported message format")
        raise ValueError("Unsupported message")


import binascii


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def hide_data(image, message):
    # Finding maximum message to store in the image.
    total_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f"Total length of message that can be encoded : {total_bytes}")

    message += "-#-#-"  # To find the end of statement when decoding.

    # Checking if the number of image bytes is greater than bytes in image.
    if len(message) > total_bytes:
        print("Insufficient bytes in image to encode the message.")
        raise ValueError("Insufficient bytes in image to encode the message.")

    message_bytes = convert_to_binary(message)
    message_length = len(message_bytes)
    index = 0

    for pixels in image:
        # pdb.set_trace()
        for pixel in pixels:
            # value for r, g, b will be returned
            color = convert_to_binary(pixel)
            for idx, x in enumerate(color):
                if index >= message_length:
                    return image
                # Lets modify the Least significant bit in the pixels
                if index < message_length:
                    # Hide the data in last bit of the red pixel
                    pixel[idx] = int(x[:-1] + message_bytes[index], 2)
                    index += 1
    return image


#  Unhide data from image
def unhide_data(image):
    decoded_msg = ""
    binary_data = ""
    for pixels in image:
        for pixel in pixels:
            for i in convert_to_binary(pixel):
                binary_data += i[-1]
                if len(binary_data) == 8:
                    decoded_msg += chr(int(str(binary_data).strip(), 2))
                    binary_data = ""
                if decoded_msg[-5:] == "-#-#-":
                    return decoded_msg[:-5]
    return decoded_msg[:-5]


#  Encode the message into image
def encode():
    image_name = input("Enter the image name (with extension) :")
    if not len(image_name):
        print("Image name is empty.")
        raise ValueError("Image name is empty.")
    image = cv2.imread(image_name)  # Read the image  using cv2 library.

    if image is None:
        print("Unable to read the image or image doesn't exist.\nPlease check the input image path.")
        sys.exit(1)

    message = input("Enter the message to encode : ")
    if not len(message):
        print("Message is empty.")
        raise ValueError("Message is empty.")

    #  Hide the data in the image and return decoded image
    steganography_image = hide_data(image, message)
    #  File name for saving the encoded image.
    steganography_image_name = input("Enter the name for new encoded image(with extension) : ")
    cv2.imwrite(f"{steganography_image_name}.png", steganography_image)  # save the encoded image


# Decode the message from image
def decode():
    steganograph_image = input("Enter the name of the steganographed image (with extension) : ")
    image = cv2.imread(steganograph_image)
    if image is None:
        print("Unable to read the image or image doesn't exist.\nPlease check the input image path.")
        sys.exit(1)
    message = unhide_data(image)
    return message


#  main function
def main():
    while True:

        user_input = int(input("Welcome to Image stenography \n 1. Enter 1 to encode the data \n"
                               " 2. Enter 2 to decode the image. \n 3. Enter 3 to Quit.\n\nEnter your input : "))

        if user_input == 1:
            print("Encoding...")
            encode()
            break

        elif user_input == 2:
            print("Decoding...")
            message = decode()
            print(f"The hidden message in the image is : \n{message}")
            break

        elif user_input == 3:
            print("Exiting...")
            break
        else:
            print("Enter the correct input.")


if __name__ == '__main__':
    #  call main function
    main()
