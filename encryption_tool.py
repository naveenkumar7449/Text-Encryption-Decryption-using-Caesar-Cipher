# -------------------------
# Text Encryption & Decryption Tool
# Using Caesar Cipher & Vigenere Cipher
# -------------------------

def caesar_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)


def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result


def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result


def main():
    print("\n===== TEXT ENCRYPTION & DECRYPTION TOOL =====")
    print("1. Caesar Cipher")
    print("2. Vigenere Cipher")
    choice = int(input("Choose a method (1/2): "))

    text = input("\nEnter your text: ")

    if choice == 1:
        key = int(input("Enter numeric key (e.g., 3): "))

        encrypted = caesar_encrypt(text, key)
        decrypted = caesar_decrypt(encrypted, key)

        print("\n--- Caesar Cipher Output ---")
        print("Encrypted Text:", encrypted)
        print("Decrypted Text:", decrypted)

    elif choice == 2:
        key = input("Enter word key (e.g., SECRET): ")

        encrypted = vigenere_encrypt(text, key)
        decrypted = vigenere_decrypt(encrypted, key)

        print("\n--- Vigenere Cipher Output ---")
        print("Encrypted Text:", encrypted)
        print("Decrypted Text:", decrypted)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()