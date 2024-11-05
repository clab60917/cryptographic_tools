from typing import List, Tuple
import numpy as np

# Constantes AES
Nb = 4  # nombre de colonnes
Nk = 4  # longueur de clé (en mots de 32 bits)
Nr = 10  # nombre de rounds

# S-box complète
sbox = [
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

# Inverse S-box
inv_sbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Rcon utilisé dans KeyExpansion
Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

# Matrice de MixColumns
mix_columns_matrix = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

# Matrice inverse de MixColumns
inv_mix_columns_matrix = [
    [0x0e, 0x0b, 0x0d, 0x09],
    [0x09, 0x0e, 0x0b, 0x0d],
    [0x0d, 0x09, 0x0e, 0x0b],
    [0x0b, 0x0d, 0x09, 0x0e]
]
def convert_to_state(input_array: List[int]) -> List[List[int]]:
    """Convertit un tableau 1D en matrice d'état AES (par colonnes)"""
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[i][j] = input_array[i + 4*j]
    return state

def convert_from_state(state: List[List[int]]) -> List[int]:
    """Convertit une matrice d'état AES en tableau 1D (par colonnes)"""
    output = []
    for j in range(4):
        for i in range(4):
            output.append(state[i][j])
    return output

def print_state(state: List[List[int]], step: str):
    """Affiche l'état actuel de la matrice de manière formatée"""
    print(f"\n{step}:")
    print("┌────┬────┬────┬────┐")
    # Affichage modifié pour refléter l'ordre des colonnes
    for i in range(4):
        print("│", end=" ")
        print(" │ ".join(f"{state[i][j]:02x}" for j in range(4)), end=" ")
        print("│")
        if i != 3:
            print("├────┼────┼────┼────┤")
    print("└────┴────┴────┴────┘")
    
    # Affichage supplémentaire pour montrer la lecture par colonnes
    print("\nLecture par colonnes:")
    columns = []
    for j in range(4):
        column = [f"{state[i][j]:02x}" for i in range(4)]
        columns.append(" ".join(column))
    print(" | ".join(columns))

def SubBytes(state: List[List[int]], inverse: bool = False) -> List[List[int]]:
    """Applique la substitution de bytes via la S-box ou son inverse"""
    box = inv_sbox if inverse else sbox
    for i in range(4):
        for j in range(4):
            state[i][j] = box[state[i][j]]
    print_state(state, "Après SubBytes" if not inverse else "Après InvSubBytes")
    return state
def ShiftRows(state: List[List[int]], inverse: bool = False) -> List[List[int]]:
    """Décale cycliquement les lignes (ou inverse)"""
    if not inverse:
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]
    else:
        state[1] = state[1][-1:] + state[1][:-1]
        state[2] = state[2][-2:] + state[2][:-2]
        state[3] = state[3][-3:] + state[3][:3]
    print_state(state, "Après ShiftRows" if not inverse else "Après InvShiftRows")
    return state

def xtime(a: int) -> int:
    """Multiplication par x dans GF(2^8)"""
    return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else a << 1

def multiply_gf(a: int, b: int) -> int:
    """Multiplication dans GF(2^8)"""
    result = 0
    for i in range(8):
        if b & 1:
            result ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1b  # Polynôme de réduction
        a &= 0xff
        b >>= 1
    return result

def MixColumns(state: List[List[int]], inverse: bool = False) -> List[List[int]]:
    """Mixage des colonnes (ou inverse) avec affichage détaillé"""
    matrix = inv_mix_columns_matrix if inverse else mix_columns_matrix
    result = [[0 for _ in range(4)] for _ in range(4)]
    
    print("\nDétail des calculs MixColumns:")
    for j in range(4):  # Pour chaque colonne
        print(f"\nColonne {j}:")
        for i in range(4):  # Pour chaque ligne de la matrice résultante
            sum_value = 0
            print(f"  Calcul de la position [{i}][{j}]:")
            for k in range(4):
                product = multiply_gf(matrix[i][k], state[k][j])
                print(f"    {hex(matrix[i][k])} × {hex(state[k][j])} = {hex(product)}")
                sum_value ^= product
            result[i][j] = sum_value
            print(f"    Résultat = {hex(sum_value)}")
    
    state = [row[:] for row in result]
    print_state(state, "Après MixColumns" if not inverse else "Après InvMixColumns")
    return state

def AddRoundKey(state: List[List[int]], round_key: List[List[int]]) -> List[List[int]]:
    """Addition de la sous-clé de round avec affichage détaillé"""
    print("\nDétail de AddRoundKey:")
    for i in range(4):
        for j in range(4):
            original = state[i][j]
            key_byte = round_key[i][j]
            state[i][j] ^= key_byte
            print(f"Position [{i}][{j}]: {hex(original)} ⊕ {hex(key_byte)} = {hex(state[i][j])}")
    
    print_state(state, "Après AddRoundKey")
    return state

def KeyExpansion(key: List[int]) -> List[List[List[int]]]:
    """Expansion de la clé avec la nouvelle organisation par colonnes"""
    w = [[] for _ in range(Nb * (Nr + 1))]
    
    print("\nExpansion de la clé:")
    print("Clé initiale:", " ".join(f"{x:02x}" for x in key))
    
    # Copie de la clé initiale par colonnes
    for i in range(Nk):
        w[i] = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]
        print(f"Colonne {i} initiale:", " ".join(f"{x:02x}" for x in w[i]))
    
    # Génération des autres mots
    for i in range(Nk, Nb * (Nr + 1)):
        temp = w[i-1].copy()
        if i % Nk == 0:
            # RotWord
            temp = temp[1:] + temp[:1]
            print(f"\nRotWord {i}:", " ".join(f"{x:02x}" for x in temp))
            
            # SubWord
            temp = [sbox[b] for b in temp]
            print(f"SubWord {i}:", " ".join(f"{x:02x}" for x in temp))
            
            # XOR avec Rcon
            temp[0] ^= Rcon[i//Nk - 1]
            print(f"After Rcon {i}:", " ".join(f"{x:02x}" for x in temp))
            
        w[i] = [w[i-Nk][j] ^ temp[j] for j in range(4)]
        print(f"Colonne {i}:", " ".join(f"{x:02x}" for x in w[i]))
    
    # Conversion en format de round keys (par colonnes)
    round_keys = []
    for i in range(Nr + 1):
        round_key = [[w[4*i+j][k] for j in range(4)] for k in range(4)]
        round_keys.append(round_key)
        print(f"\nRound key {i}:")
        print_state(round_key, f"Round key {i}")
    
    return round_keys
def AES_Encrypt(plaintext: List[int], key: List[int]) -> List[int]:
    """
    Chiffrement AES complet avec affichage détaillé de chaque étape
    La matrice d'état est organisée par colonnes
    """
    print("\n=== DÉBUT DU CHIFFREMENT AES ===")
    print("\nPlaintext (par colonnes):", " ".join(f"{x:02x}" for x in plaintext))
    print("Key (par colonnes):", " ".join(f"{x:02x}" for x in key))
    
    # Conversion du plaintext en state array (par colonnes)
    state = convert_to_state(plaintext)
    print("\nState Array initial (lecture par colonnes):")
    print_state(state, "État initial")
    
    # Key expansion
    round_keys = KeyExpansion(key)
    
    # Round initial
    print("\n=== ROUND INITIAL ===")
    state = AddRoundKey(state, round_keys[0])
    
    # Rounds principaux
    for round in range(1, Nr):
        print(f"\n=== ROUND {round} ===")
        print("\nÉtat au début du round:")
        print_state(state, f"Début round {round}")
        
        print("\nSubBytes:")
        state = SubBytes(state)
        
        print("\nShiftRows:")
        state = ShiftRows(state)
        
        print("\nMixColumns:")
        state = MixColumns(state)
        
        print("\nAddRoundKey:")
        state = AddRoundKey(state, round_keys[round])
    
    # Round final
    print(f"\n=== ROUND FINAL (ROUND {Nr}) ===")
    print("\nÉtat au début du round final:")
    print_state(state, "Début round final")
    
    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, round_keys[Nr])
    
    # Conversion du state array en sortie (par colonnes)
    result = convert_from_state(state)
    print("\nRésultat final (par colonnes):", " ".join(f"{x:02x}" for x in result))
    return result

def AES_Decrypt(ciphertext: List[int], key: List[int]) -> List[int]:
    """
    Déchiffrement AES complet avec affichage détaillé de chaque étape
    La matrice d'état est organisée par colonnes
    """
    print("\n=== DÉBUT DU DÉCHIFFREMENT AES ===")
    print("\nCiphertext (par colonnes):", " ".join(f"{x:02x}" for x in ciphertext))
    print("Key (par colonnes):", " ".join(f"{x:02x}" for x in key))
    
    # Conversion du ciphertext en state array (par colonnes)
    state = convert_to_state(ciphertext)
    print("\nState Array initial (lecture par colonnes):")
    print_state(state, "État initial")
    
    # Key expansion
    round_keys = KeyExpansion(key)
    
    # Round initial
    print("\n=== ROUND INITIAL ===")
    state = AddRoundKey(state, round_keys[Nr])
    state = ShiftRows(state, inverse=True)
    state = SubBytes(state, inverse=True)
    
    # Rounds principaux
    for round in range(Nr-1, 0, -1):
        print(f"\n=== ROUND {Nr-round} ===")
        print("\nÉtat au début du round:")
        print_state(state, f"Début round {Nr-round}")
        
        state = AddRoundKey(state, round_keys[round])
        state = MixColumns(state, inverse=True)
        state = ShiftRows(state, inverse=True)
        state = SubBytes(state, inverse=True)
    
    # Round final
    print(f"\n=== ROUND FINAL ===")
    state = AddRoundKey(state, round_keys[0])
    
    # Conversion du state array en sortie (par colonnes)
    result = convert_from_state(state)
    print("\nRésultat final (par colonnes):", " ".join(f"{x:02x}" for x in result))
    return result
def test_AES():
    """Fonction de test avec choix du type d'entrée et du mode"""
    
    # Configuration de la sortie vers fichier et console
    import sys
    original_stdout = sys.stdout
    
    with open('aes_output.txt', 'w', encoding='utf-8') as f:
        class MultiWriter:
            def write(self, text):
                f.write(text)
                original_stdout.write(text)
            def flush(self):
                f.flush()
                original_stdout.flush()
        
        sys.stdout = MultiWriter()

        print("================ TEST AES ================")
        print("\nChoisissez le mode :")
        print("1. Test AES complet")
        print("2. Mode simplifié (uniquement SubBytes, ShiftRows, MixColumns)")
        
        mode = input("Votre choix (1-2): ")

        print("\nChoisissez le type d'entrée :")
        print("1. Entrée hexadécimale prédéfinie")
        print("2. Entrée texte")
        print("3. Entrée hexadécimale personnalisée")
        print("4. État exercice 2")
        
        choice = input("Votre choix (1-4): ")

        # Définir l'état initial selon le choix
        if choice == '1':
            # Matrice d'entrée organisée par colonnes
            input_matrix = [
                0x00, 0x11, 0x22, 0x33,  # première colonne
                0x44, 0x55, 0x66, 0x77,  # deuxième colonne
                0x88, 0x99, 0xaa, 0xbb,  # troisième colonne
                0xcc, 0xdd, 0xee, 0xff   # quatrième colonne
            ]
            state = convert_to_state(input_matrix)
            test_name = "TEST ENTRÉE HEXADÉCIMALE PRÉDÉFINIE"

        elif choice == '2':
            print("\nEntrez votre texte (16 caractères max):")
            message = input()
            text = [ord(c) for c in message.ljust(16)]
            state = convert_to_state(text)
            test_name = "TEST ENTRÉE TEXTE"

        elif choice == '3':
            print("\nEntrez votre chaîne hexadécimale pour les colonnes (32 caractères, ex: 000102...)")
            print("Format: première colonne, puis deuxième, etc.")
            hex_string = input()
            try:
                text = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
                if len(text) != 16:
                    raise ValueError("La longueur doit être de 16 octets")
                state = convert_to_state(text)
            except Exception as e:
                print(f"Erreur: {e}")
                sys.stdout = original_stdout
                return
            test_name = "TEST ENTRÉE HEXADÉCIMALE PERSONNALISÉE"

        elif choice == '4':
            # État de l'exercice 2 organisé par colonnes
            input_matrix = [
                0x12, 0xcf, 0x21, 0xde,  # première colonne
                0x00, 0xa4, 0xf4, 0x05,  # deuxième colonne
                0xc6, 0x4e, 0xa9, 0x78,  # troisième colonne
                0x82, 0xec, 0x6b, 0x60   # quatrième colonne
            ]
            state = convert_to_state(input_matrix)
            test_name = "TEST EXERCICE 2"

        else:
            print("Choix invalide")
            sys.stdout = original_stdout
            return

        if mode == '2':
            # Mode simplifié : uniquement SubBytes, ShiftRows, MixColumns
            print(f"\n{'='*20} DÉBUT {test_name} {'='*20}")
            print("\nÉtat initial (lecture par colonnes):")
            print_state(state, "Initial")
            
            # 1. SubBytes
            print("\n=== ÉTAPE 1: SubBytes ===")
            state_after_subbytes = SubBytes(state.copy())
            
            # 2. ShiftRows
            print("\n=== ÉTAPE 2: ShiftRows ===")
            state_after_shiftrows = ShiftRows(state_after_subbytes.copy())
            
            # 3. MixColumns
            print("\n=== ÉTAPE 3: MixColumns ===")
            print("Calculs détaillés pour MixColumns:")
            state_after_mixcolumns = MixColumns(state_after_shiftrows.copy())

        else:
            # Mode complet AES
            # Convertir state en plaintext (par colonnes)
            plaintext = convert_from_state(state)
            
            # Clé commune (organisée par colonnes)
            key = [
                0x00, 0x04, 0x08, 0x0c,  # première colonne
                0x01, 0x05, 0x09, 0x0d,  # deuxième colonne
                0x02, 0x06, 0x0a, 0x0e,  # troisième colonne
                0x03, 0x07, 0x0b, 0x0f   # quatrième colonne
            ]

            print(f"\n{'='*20} DÉBUT {test_name} {'='*20}")
            print(f"\nPlaintext (hex, par colonnes): {' '.join(f'{x:02x}' for x in plaintext)}")
            print(f"Key (hex, par colonnes): {' '.join(f'{x:02x}' for x in key)}")
            
            # Chiffrement
            ciphertext = AES_Encrypt(plaintext, key)
            
            # Déchiffrement
            decrypted = AES_Decrypt(ciphertext, key)
            
            # Vérification
            print(f"\n{'='*20} VÉRIFICATION {test_name} {'='*20}")
            print(f"Plaintext original (hex): {' '.join(f'{x:02x}' for x in plaintext)}")
            print(f"Texte déchiffré (hex):   {' '.join(f'{x:02x}' for x in decrypted)}")
            print(f"Test {'réussi' if plaintext == decrypted else 'échoué'}!")
            print(f"{'='*50}")

        # Restaurer la sortie standard
        sys.stdout = original_stdout

    print("\nRésultats complets sauvegardés dans aes_output.txt")

if __name__ == "__main__":
    # Configuration de l'affichage du terminal
    import os
    if os.name == 'nt':  # Windows
        os.system('mode con: cols=200 lines=5000')
    
    # Désactive la limite d'affichage de Python
    import sys
    sys.set_int_max_str_digits(0)
    
    try:
        test_AES()
        input("\nAppuyez sur Enter pour quitter...")
    except KeyboardInterrupt:
        print("\n\nSimulation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        input("\nAppuyez sur Enter pour quitter...")