from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

# Table S-Box (complète-la avec les valeurs correctes)
s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  
  0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  
  0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  
  0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  
  0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  
  0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  
  0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  
  0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  
  0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  
  0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  
  0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  
  0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  
  0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  
  0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  
  0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  
  0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 
]

def format_bytes(byte_data):
    """Format bytes in a readable hexadecimal format."""
    return ' '.join([f"{b:02x}" for b in byte_data])

def aes_encrypt_with_steps(plaintext, key):
    """Chiffrement AES qui imprime chaque étape des rounds de chiffrement"""
    backend = default_backend()

    # Initialisation du chiffreur AES
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()

    # Diviser le plaintext en blocs de 16 octets (128 bits)
    block_size = 16
    plaintext_blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]

    print("\n--- Détails du chiffrement AES ---")

    for block_num, block in enumerate(plaintext_blocks):
        print(f"\nBloc {block_num + 1}:")
        print(f"Plaintext initial : {format_bytes(block)}")

        # Ajouter du padding si nécessaire
        if len(block) < block_size:
            padding_length = block_size - len(block)
            block += bytes([padding_length] * padding_length)
            print(f"Plaintext après padding : {format_bytes(block)}")

        # Clé initiale et état initial
        state = block
        print(f"État initial : {format_bytes(state)}")

        # Simuler chaque round d'AES (nombre de rounds dépend de la taille de la clé)
        num_rounds = {
            16: 10,  # AES-128
            24: 12,  # AES-192
            32: 14   # AES-256
        }[len(key)]

        # Clé initiale ajoutée (round key 0)
        state = xor_bytes(state, key[:block_size])
        print(f"Après ajout de la clé de round 0 : {format_bytes(state)}")

        for round_num in range(1, num_rounds + 1):
            print(f"\n--- Round {round_num} ---")

            # SubBytes (Substitution des octets)
            state = sub_bytes(state)
            print(f"Après SubBytes : {format_bytes(state)}")

            # ShiftRows (Décalage des lignes)
            state = shift_rows(state)
            print(f"Après ShiftRows : {format_bytes(state)}")

            # MixColumns (Mélange des colonnes, sauf le dernier round)
            if round_num < num_rounds:
                state = mix_columns(state)
                print(f"Après MixColumns : {format_bytes(state)}")

            # AddRoundKey (Ajout de la clé de round)
            round_key = key_schedule(key, round_num)  # Générer la clé de round
            state = xor_bytes(state, round_key)
            print(f"Après AddRoundKey {round_num} : {format_bytes(state)}")

    # Effectuer le chiffrement complet et afficher le résultat final
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    print("\n--- Chiffrement terminé ---")
    print(f"Texte chiffré final : {format_bytes(ciphertext)}")

    return ciphertext

def xor_bytes(a, b):
    """XOR entre deux byte strings de même longueur"""
    return bytes(x ^ y for x, y in zip(a, b))

def sub_bytes(state):
    """SubBytes - substitution de chaque octet en utilisant la table S-Box AES"""
    return bytes(s_box[byte] for byte in state)

def shift_rows(state):
    """ShiftRows - décalage des lignes dans l'état"""
    state_matrix = [list(state[i::4]) for i in range(4)]
    for i in range(1, 4):
        state_matrix[i] = state_matrix[i][i:] + state_matrix[i][:i]  # Décalage circulaire
    return bytes(sum(state_matrix, []))

def mix_columns(state):
    """MixColumns - multiplication matricielle pour mélanger les colonnes"""
    def xtime(a):
        return ((a << 1) ^ 0x1b) if (a & 0x80) else (a << 1)

    def mix_single_column(column):
        t = column[0] ^ column[1] ^ column[2] ^ column[3]
        u = column[0]
        column[0] ^= t ^ xtime(column[0] ^ column[1])
        column[1] ^= t ^ xtime(column[1] ^ column[2])
        column[2] ^= t ^ xtime(column[2] ^ column[3])
        column[3] ^= t ^ xtime(column[3] ^ u)
        return [c & 0xff for c in column]  # S'assurer que les valeurs restent dans la plage des octets

    columns = [list(state[i::4]) for i in range(4)]
    mixed_columns = [mix_single_column(col) for col in columns]
    return bytes(sum(mixed_columns, []))

def key_schedule(key, round_num):
    """Génère la clé de round pour AddRoundKey"""
    rcon = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
    ]

    def sub_word(word):
        """Substitution de mot avec la S-Box"""
        return bytes([s_box[b] for b in word])

    def rot_word(word):
        """Rotation de mot (1 octet à gauche)"""
        return word[1:] + word[:1]

    key_columns = [key[i:i + 4] for i in range(0, len(key), 4)]
    for i in range(len(key_columns), 4 * (round_num + 1)):
        temp = key_columns[-1]
        if i % 4 == 0:
            temp = bytes(a ^ b for a, b in zip(sub_word(rot_word(temp)), [rcon[i // 4 - 1], 0x00, 0x00, 0x00]))
        key_columns.append(bytes(a ^ b for a, b in zip(key_columns[i - 4], temp)))

    return b''.join(key_columns[4 * round_num:4 * (round_num + 1)])

if __name__ == "__main__":
    # Entrer la clé et le texte en clair
    key_input = input("Entrez la clé (en hexadécimal, 32, 48, ou 64 caractères): ")
    plaintext_input = input("Entrez le texte à chiffrer (en clair): ")

    # Convertir la clé et le texte en clair en bytes
    key = bytes.fromhex(key_input)
    plaintext = plaintext_input.encode()

    # Appeler la fonction de chiffrement
    aes_encrypt_with_steps(plaintext, key)
