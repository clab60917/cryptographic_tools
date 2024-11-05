def get_lfsr_size():
    """Demande la taille du LFSR"""
    while True:
        print("\nChoisissez la taille du LFSR (4 ou 5):")
        try:
            size = int(input("Taille: ").strip())
            if size not in [4, 5]:
                print("Erreur: La taille doit être 4 ou 5")
                continue
            return size
        except ValueError:
            print("Erreur: Veuillez entrer un nombre")

def get_initial_state(size):
    """Demande et valide l'état initial du LFSR"""
    while True:
        print(f"\nEntrez l'état initial du LFSR ({size} bits séparés par des espaces ou des virgules)")
        print(f"Example: {'1 ' * size}ou{'1,' * (size-1)}1")
        print(f"Ou appuyez sur Enter pour utiliser l'état par défaut ({'1,' * (size-1)}1)")
        
        user_input = input("État initial: ").strip()
        
        # Utiliser l'état par défaut si rien n'est entré
        if not user_input:
            default_state = [1] * size
            print(f"\nUtilisation de l'état par défaut: {default_state}")
            return default_state
        
        # Nettoyer et parser l'entrée
        try:
            # Accepte les entrées séparées par des espaces ou des virgules
            if ',' in user_input:
                bits = [int(bit.strip()) for bit in user_input.split(',')]
            else:
                bits = [int(bit) for bit in user_input.split()]
            
            # Vérifier la longueur
            if len(bits) != size:
                print(f"Erreur: Il faut exactement {size} bits")
                continue
            
            # Vérifier que ce sont bien des bits (0 ou 1)
            if not all(bit in [0, 1] for bit in bits):
                print("Erreur: Les valeurs doivent être 0 ou 1")
                continue
            
            print(f"\nÉtat initial choisi: {bits}")
            return bits
            
        except ValueError:
            print("Erreur: Entrée invalide. Utilisez uniquement des 0 et des 1")

def get_polynomial():
    """Demande le polynôme de rétroaction"""
    print("\nEntrez le polynôme de rétroaction sous forme de liste de termes (ex: 5,2,0 pour T⁵ ⊕ T² ⊕ 1)")
    print("Chaque terme représente un coefficient non nul, le terme constant doit être 0.")
    
    while True:
        try:
            polynomial_input = input("Polynôme: ").strip()
            polynomial = [int(term.strip()) for term in polynomial_input.split(',')]
            
            if all(coef >= 0 for coef in polynomial):
                print(f"Polynôme choisi: {polynomial}")
                return polynomial
            else:
                print("Erreur: Les termes doivent être des entiers positifs ou nuls.")
        except ValueError:
            print("Erreur: Entrée invalide. Veuillez entrer des entiers séparés par des virgules.")

class LFSR_Simulator:
    def __init__(self, initial_state, size, polynomial):
        self.state = initial_state
        self.size = size
        self.polynomial = polynomial  # Nouvelle propriété pour le polynôme
        self.states_history = [initial_state.copy()]

    def next_bit(self):
        """Calcule le prochain bit de rétroaction en utilisant le polynôme de rétroaction personnalisé"""
        feedback = 0
        print("\nCalcul du bit de rétroaction:")
        for term in self.polynomial:
            if term < self.size:
                feedback ^= self.state[term]
                print(f"Terme T^{term + 1}: {self.state[term]}")
        
        print(f"Bit de rétroaction calculé: {feedback}")
        return feedback

    def step(self):
        """Effectue un pas de l'évolution du LFSR avec détails"""
        print("\n" + "="*50)
        print(f"État actuel: {self.state}")
        
        # Calcul du bit de rétroaction
        feedback = self.next_bit()
        
        # Décalage vers la gauche avec détails
        print("\nDécalage vers la gauche:")
        print(f"Ancien état: {self.state}")
        new_state = self.state[1:] + [feedback]
        print(f"Nouveau état après décalage: {new_state}")
        print(f"Bit de rétroaction inséré à droite: {feedback}")
        
        # Mise à jour de l'état
        self.state = new_state
        self.states_history.append(new_state.copy())
        
        return self.state

def gpa_output(state, size):
    """Calcule le bit de sortie du GPA avec détails des calculs"""
    if size == 5:
        x2, x3, x4 = state[1], state[2], state[3]
        result = (1 + x4 + x2*x3) & 1
        print(f"\nCalcul du bit GPA (taille 5):")
        print(f"f(u,v,w) = 1 + w + uv avec:")
        print(f"u = x2 = {x2}")
        print(f"v = x3 = {x3}")
        print(f"w = x4 = {x4}")
        print(f"f = 1 + {x4} + ({x2}×{x3}) = {result}")
    else:  # size == 4
        x1, x2, x3 = state[0], state[1], state[2]
        result = (1 + x3 + x1*x2) & 1
        print(f"\nCalcul du bit GPA (taille 4):")
        print(f"f(u,v,w) = 1 + w + uv avec:")
        print(f"u = x1 = {x1}")
        print(f"v = x2 = {x2}")
        print(f"w = x3 = {x3}")
        print(f"f = 1 + {x3} + ({x1}×{x2}) = {result}")
    return result

def detect_period(states):
    """Détecte la période dans une séquence d'états"""
    n = len(states)
    for period in range(1, n):
        is_periodic = True
        # On vérifie si la séquence se répète avec cette période
        for i in range(n - period):
            if i + period < n and states[i] != states[i + period]:
                is_periodic = False
                break
        if is_periodic:
            print(f"\nDétection de période:")
            print(f"Période trouvée: {period}")
            print(f"Séquence qui se répète: {states[:period]}")
            return period
    return None

def print_state_details(t, state, gpa_bit=None):
    """Affiche les détails d'un état avec formatage amélioré"""
    state_str = "".join(map(str, state))
    state_formatted = f"({', '.join(map(str, state))})"
    if gpa_bit is not None:
        print(f"\nX_{t} = {state_formatted}")
        print(f"Format binaire: {state_str}")
        print(f"Bit de sortie GPA z_{t} = {gpa_bit}")
    else:
        print(f"\nX_{t} = {state_formatted}")
        print(f"Format binaire: {state_str}")

def save_to_file(states, gpa_bits, period, size):
    """Sauvegarde les résultats dans un fichier"""
    with open('lfsr_results.txt', 'w') as f:
        f.write(f"=== RÉSULTATS SIMULATION LFSR (TAILLE {size}) ===\n\n")
        
        f.write("États:\n")
        for i, state in enumerate(states):
            f.write(f"X_{i} = {state}\n")
        
        f.write("\nBits de sortie GPA:\n")
        f.write("z = " + "".join(map(str, gpa_bits)) + "\n")
        
        f.write(f"\nPériode détectée: {period}\n")
        f.write(f"Période maximale théorique: 2^{size} - 1 = {2**size - 1}\n")

def main():
    # Demander la taille du LFSR
    size = get_lfsr_size()
    
    # Demander l'état initial
    initial_state = get_initial_state(size)
    
    # Demander le polynôme de rétroaction
    polynomial = get_polynomial()
    
    # Initialisation
    lfsr = LFSR_Simulator(initial_state, size, polynomial)
    
    print("="*60)
    print("SIMULATION LFSR ET GPA")
    print("="*60)
    
    print("\nParamètres:")
    print(f"- Taille du LFSR: {size} cellules")
    print(f"- Polynôme de rétroaction: {', '.join([f'T^{term + 1}' for term in polynomial])}")
    print(f"- État initial: {initial_state}")
    
    # Question 2: Calculer X₁,...,X₁₀
    print("\n" + "="*20 + " ÉVOLUTION DES ÉTATS " + "="*20)
    states = []
    gpa_bits = []
    
    # État initial
    print("\nÉtat initial:")
    print_state_details(0, lfsr.state)
    states.append(lfsr.state.copy())
    gpa_bits.append(gpa_output(lfsr.state, size))
    
    # Calcul des états suivants
    for t in range(1, 11):
        print(f"\n{'-'*20} Étape {t} {'-'*20}")
        current_state = lfsr.step()
        states.append(current_state.copy())
        gpa_bits.append(gpa_output(current_state, size))
        print_state_details(t, current_state)
    
    # Détection et analyse de la période
    print("\n" + "="*20 + " ANALYSE DE LA PÉRIODE " + "="*20)
    print(f"\nPériode maximale théorique: 2^{size} - 1 = {2**size - 1}")
    
    period = detect_period(states)
    if period:
        print(f"Période effective détectée: {period}")
        print("\nDémonstration de la périodicité:")
        for i in range(period):
            print(f"État {i}: {states[i]} se répète à l'état {i+period}: {states[i+period]}")
    
    # Bits de sortie du GPA
    print("\n" + "="*20 + " BITS DE SORTIE DU GPA " + "="*20)
    print("\nSéquence complète des bits de sortie:")
    print("z = ", end="")
    for i, bit in enumerate(gpa_bits):
        print(bit, end="")
        if (i+1) % 5 == 0:  # Groupe par 5 pour la lisibilité
            print(" ", end="")
    print("\n")
    
    # Sauvegarde des résultats
    try:
        save_to_file(states, gpa_bits, period, size)
        print("\nLes résultats ont été sauvegardés dans 'lfsr_results.txt'")
    except Exception as e:
        print(f"\nErreur lors de la sauvegarde des résultats: {e}")

    print("\n" + "="*20 + " FIN DE LA SIMULATION " + "="*20)

if __name__ == "__main__":
    # Configuration de l'affichage du terminal
    import os
    if os.name == 'nt':  # Windows
        os.system('mode con: cols=200 lines=5000')
    
    # Désactive la limite d'affichage de Python
    import sys
    sys.set_int_max_str_digits(0)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
    
    input("\nAppuyez sur Enter pour quitter...")
