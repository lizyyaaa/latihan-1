import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Function to upload file and read content
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, text)

# Function to handle Vigenere encryption
def vigenere_encrypt(plaintext, key):
    key = key.lower()
    ciphertext = ""
    key_len = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('a')
            if char.isupper():
                ciphertext += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                ciphertext += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            ciphertext += char
    return ciphertext

# Function to handle Playfair encryption
def playfair_encrypt(plaintext, key):
    key = key.lower().replace("j", "i")  # replace J with I for simplicity
    matrix = create_playfair_matrix(key)
    pairs = create_playfair_pairs(plaintext)
    ciphertext = ""
    for pair in pairs:
        ciphertext += encrypt_playfair_pair(pair, matrix)
    return ciphertext

def create_playfair_matrix(key):
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    matrix = []
    for char in key:
        if char not in matrix:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def create_playfair_pairs(plaintext):
    plaintext = plaintext.lower().replace("j", "i")
    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:
                pairs.append((a, 'x'))
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        else:
            pairs.append((a, 'x'))
            i += 1
    return pairs

def encrypt_playfair_pair(pair, matrix):
    a, b = pair
    row_a, col_a = divmod(matrix.index(a), 5)
    row_b, col_b = divmod(matrix.index(b), 5)
    if row_a == row_b:
        return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
    elif col_a == col_b:
        return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
    else:
        return matrix[row_a][col_b] + matrix[row_b][col_a]

# Function to handle Hill encryption
def hill_encrypt(plaintext, key_matrix):
    key_matrix = np.array(key_matrix)
    ciphertext = ""
    plaintext = plaintext.lower().replace(" ", "")
    plaintext = [ord(c) - ord('a') for c in plaintext if c.isalpha()]
    while len(plaintext) % key_matrix.shape[0] != 0:
        plaintext.append(ord('x') - ord('a'))
    
    plaintext_matrix = np.reshape(plaintext, (-1, key_matrix.shape[0]))
    for row in plaintext_matrix:
        encrypted_row = np.dot(key_matrix, row) % 26
        ciphertext += ''.join(chr(int(val) + ord('a')) for val in encrypted_row)
    
    return ciphertext

# Function to perform encryption based on user choice
def encrypt():
    plaintext = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    
    if len(key) < 12:
        messagebox.showerror("Error", "Key must be at least 12 characters long.")
        return

    cipher_type = cipher_var.get()
    
    if cipher_type == "Vigenere":
        result = vigenere_encrypt(plaintext, key)
    elif cipher_type == "Playfair":
        result = playfair_encrypt(plaintext, key)
    elif cipher_type == "Hill":
        key_matrix = [[2, 4, 5], [9, 2, 1], [3, 17, 7]]  # Example key matrix
        result = hill_encrypt(plaintext, key_matrix)
    else:
        result = "Invalid cipher selected."
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

# GUI setup
root = tk.Tk()
root.title("Encryption Program")

# Input text
input_label = tk.Label(root, text="Input Text:")
input_label.pack()
input_text = tk.Text(root, height=10, width=50)
input_text.pack()

# Upload file button
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack()

# Key input
key_label = tk.Label(root, text="Enter Key (min. 12 characters):")
key_label.pack()
key_entry = tk.Entry(root, width=50)
key_entry.pack()

# Cipher selection
cipher_var = tk.StringVar(value="Vigenere")
cipher_label = tk.Label(root, text="Select Cipher:")
cipher_label.pack()

cipher_menu = tk.OptionMenu(root, cipher_var, "Vigenere", "Playfair", "Hill")
cipher_menu.pack()

# Encrypt button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack()

# Output text
output_label = tk.Label(root, text="Output Text:")
output_label.pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
