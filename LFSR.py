class LFSR_Simulator:
    def __init__(self, initial_state, feedback_polynomial):
        self.state = initial_state
        self.size = len(initial_state)
        self.feedback_polynomial = feedback_polynomial
        self.states_history = [initial_state.copy()]
    
    def next_bit(self):
        """Calcule le prochain bit de rétroaction selon le polynôme T⁵ ⊕ T² ⊕ 1"""
        feedback = (self.state[0] ^ self.state[3] ^ 1) & 1
        print(f"\nCalcul du bit de rétroaction:")
        print(f"T⁵ terme: {self.state[0]}")
        print(f"T² terme: {self.state[3]}")
        print(f"1 terme: 1")
        print(f"feedback = {self.state[0]} ⊕ {self.state[3]} ⊕ 1 = {feedback}")
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

def get_initial_state():
    """Demande et valide l'état initial du LFSR"""
    while True:
        print("\nEntrez l'état initial du LFSR (5 bits séparés par des espaces ou des virgules)")
        print("Example: 1 1 1 1 1 ou 1,1,1,1,1")
        print("Ou appuyez sur Enter pour utiliser l'état par défaut (1,1,1,1,1)")
        
        user_input = input("État initial: ").strip()
        
        # Utiliser l'état par défaut si rien n'est entré
        if not user_input:
            print("\nUtilisation de l'état par défaut: [1, 1, 1, 1, 1]")
            return [1, 1, 1, 1, 1]
        
        # Nettoyer et parser l'entrée
        try:
            # Accepte les entrées séparées par des espaces ou des virgules
            if ',' in user_input:
                bits = [int(bit.strip()) for bit in user_input.split(',')]
            else:
                bits = [int(bit) for bit in user_input.split()]
            
            # Vérifier la longueur
            if len(bits) != 5:
                print("Erreur: Il faut exactement 5 bits")
                continue
            
            # Vérifier que ce sont bien des bits (0 ou 1)
            if not all(bit in [0, 1] for bit in bits):
                print("Erreur: Les valeurs doivent être 0 ou 1")
                continue
            
            print(f"\nÉtat initial choisi: {bits}")
            return bits
            
        except ValueError:
            print("Erreur: Entrée invalide. Utilisez uniquement des 0 et des 1")
            
def gpa_output(state):
    """Calcule le bit de sortie du GPA avec détails des calculs"""
    x2, x3, x4 = state[1], state[2], state[3]
    result = (1 + x4 + x2*x3) & 1
    print(f"\nCalcul du bit GPA:")
    print(f"f(u,v,w) = 1 + w + uv avec:")
    print(f"u = x2 = {x2}")
    print(f"v = x3 = {x3}")
    print(f"w = x4 = {x4}")
    print(f"f = 1 + {x4} + ({x2}×{x3}) = {result}")
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

def save_to_file(states, gpa_bits, period):
    """Sauvegarde les résultats dans un fichier"""
    with open('lfsr_results.txt', 'w') as f:
        f.write("=== RÉSULTATS SIMULATION LFSR ===\n\n")
        
        f.write("États:\n")
        for i, state in enumerate(states):
            f.write(f"X_{i} = {state}\n")
        
        f.write("\nBits de sortie GPA:\n")
        f.write("z = " + "".join(map(str, gpa_bits)) + "\n")
        
        f.write(f"\nPériode détectée: {period}\n")

def main():
    # Demander l'état initial
    initial_state = get_initial_state()
    
    # Initialisation
    lfsr = LFSR_Simulator(initial_state, "T⁵ ⊕ T² ⊕ 1")
    
    print("="*60)
    print("SIMULATION LFSR ET GPA")
    print("="*60)
    
    print("\nParamètres:")
    print(f"- Taille du LFSR: 5 cellules")
    print(f"- Polynôme de rétroaction: T⁵ ⊕ T² ⊕ 1")
    print(f"- État initial: {initial_state}")
    
    # Question 2: Calculer X₁,...,X₁₀
    print("\n" + "="*20 + " ÉVOLUTION DES ÉTATS " + "="*20)
    states = []
    gpa_bits = []
    
    # État initial
    print("\nÉtat initial:")
    print_state_details(0, lfsr.state)
    states.append(lfsr.state.copy())
    gpa_bits.append(gpa_output(lfsr.state))
    
    # Calcul des états suivants
    for t in range(1, 11):
        print(f"\n{'-'*20} Étape {t} {'-'*20}")
        current_state = lfsr.step()
        states.append(current_state.copy())
        gpa_bits.append(gpa_output(current_state))
        print_state_details(t, current_state)
    
    # Détection et analyse de la période
    print("\n" + "="*20 + " ANALYSE DE LA PÉRIODE " + "="*20)
    print(f"\nPériode maximale théorique: 2^5 - 1 = {2**5 - 1}")
    
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
        save_to_file(states, gpa_bits, period)
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
    