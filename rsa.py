def extended_gcd(a, b):
    """Algorithme d'Euclide étendu pour trouver l'identité de Bezout"""
    print(f"\nCalcul de l'identité de Bezout pour {a} et {b}")
    if a == 0:
        print(f"a = 0, donc gcd({a}, {b}) = {b}")
        return b, 0, 1
    
    # Sauvegarde des valeurs initiales pour l'affichage
    original_a, original_b = a, b
    
    # Tableau pour stocker les étapes de la division euclidienne
    steps = []
    while a != 0:
        q = b // a
        r = b % a
        steps.append((b, a, q, r))
        b = a
        a = r
    
    print("\nDivisions euclidiennes successives:")
    print("b  = a × q + r")
    print("-" * 40)
    for step in steps:
        print(f"{step[0]} = {step[1]} × {step[2]} + {step[3]}")
    
    # Calcul des coefficients de Bezout
    x, y = 0, 1
    u, v = 1, 0
    for step in reversed(steps[:-1]):
        q = step[2]
        x, u = u, x - q * u
        y, v = v, y - q * v
    
    print(f"\nIdentité de Bezout:")
    print(f"{original_a} × ({x}) + {original_b} × ({y}) = {b}")
    
    return b, x, y

def find_factors(n):
    """Trouve les facteurs d'un nombre n avec détail des tests"""
    print(f"\nRecherche des facteurs de {n}:")
    for i in range(2, n):
        if n % i == 0:
            print(f"Test de {i} : {n} ÷ {i} = {n//i} (reste {n%i})")
            print(f"→ {i} est un facteur de {n}")
            return [i, n//i]
        else:
            print(f"Test de {i} : {n} ÷ {i} = {n//i} (reste {n%i})")
    return None

def calculate_phi(p, q):
    """Calcule φ(n) avec détail"""
    print(f"\nCalcul de φ(n) = (p-1)(q-1):")
    print(f"p-1 = {p}-1 = {p-1}")
    print(f"q-1 = {q}-1 = {q-1}")
    phi = (p-1) * (q-1)
    print(f"φ(n) = {p-1} × {q-1} = {phi}")
    return phi

def rsa_encrypt(m, e, n):
    """Chiffrement RSA avec détail des calculs"""
    print(f"\nCalcul de c = m^e mod n:")
    print(f"m = {m}")
    print(f"e = {e}")
    print(f"n = {n}")
    
    # Exponentiation modulaire détaillée
    result = pow(m, e, n)
    print(f"c = {m}^{e} mod {n} = {result}")
    return result

def rsa_decrypt(c, d, n):
    """Déchiffrement RSA avec détail des calculs"""
    print(f"\nCalcul de m = c^d mod n:")
    print(f"c = {c}")
    print(f"d = {d}")
    print(f"n = {n}")
    
    # Exponentiation modulaire détaillée
    result = pow(c, d, n)
    print(f"m = {c}^{d} mod {n} = {result}")
    return result

def find_d(e, phi):
    """Trouve d avec l'algorithme d'Euclide étendu détaillé"""
    print(f"\nRecherche de d tel que ed ≡ 1 (mod φ(n)):")
    print(f"e = {e}")
    print(f"φ(n) = {phi}")
    
    gcd, d, y = extended_gcd(e, phi)
    if gcd != 1:
        print(f"ERREUR: e n'est pas premier avec φ(n)")
        return None
    
    d = d % phi
    print(f"\nL'exposant d est donc: {d}")
    print(f"Vérification: {e} × {d} ≡ {(e*d)} ≡ {(e*d)%phi} (mod {phi})")
    return d

def exercice_3():
    print("="*50)
    print("EXERCICE 3: RSA")
    print("="*50)
    
    # Paramètres donnés
    n = 4331
    e = 59
    m1 = 3158
    c2 = 167
    p = 61
    
    print("\nParamètres donnés:")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"m1 = {m1}")
    print(f"c2 = {c2}")
    print(f"p = {p}")

    print("\n" + "="*20 + " QUESTION 1 " + "="*20)
    print("Calcul du chiffré c1 pour m1 = 110")
    c1 = rsa_encrypt(m1, e, n)

    print("\n" + "="*20 + " QUESTION 2 " + "="*20)
    print(f"Vérification que {p} est facteur de {n} et calcul de φ(n)")
    if n % p == 0:
        q = n // p
        print(f"\nVérification de la factorisation:")
        print(f"{p} × {q} = {n}")
        print(f"donc {p} est bien un facteur de {n}")
        phi = calculate_phi(p, q)
    else:
        print(f"{p} n'est pas un facteur de {n}")
        return

    print("\n" + "="*20 + " QUESTION 3 " + "="*20)
    print("Calcul de l'exposant de déchiffrement d")
    d = find_d(e, phi)

    print("\n" + "="*20 + " QUESTION 4 " + "="*20)
    print(f"Déchiffrement de c2 = {c2}")
    m2 = rsa_decrypt(c2, d, n)

    print("\n" + "="*20 + " RÉCAPITULATIF " + "="*20)
    print(f"1. c1 = {c1}")
    print(f"2. φ(n) = {phi}")
    print(f"3. d = {d}")
    print(f"4. m2 = {m2}")

if __name__ == "__main__":
    exercice_3()