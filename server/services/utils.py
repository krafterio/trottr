def get_ctr_by_position(position: int) -> float:
    """
    Retourne le CTR (Click-Through Rate) moyen en fonction de la position Google
    
    Args:
        position: Position dans les résultats de recherche Google
        
    Returns:
        Taux de clic moyen en pourcentage (valeur décimale entre 0 et 1)
    """
    if position is None:
        return 0
        
    # Tableau des taux de clic moyens par position
    ctr_data = {
        1: 0.310,  # 31.0%
        2: 0.247,  # 24.7%
        3: 0.186,  # 18.6%
        4: 0.136,  # 13.6%
        5: 0.095,  # 9.5%
        6: 0.062,  # 6.2%
        7: 0.043,  # 4.3%
        8: 0.031,  # 3.1%
        9: 0.026,  # 2.6%
        10: 0.024,  # 2.4%
    }
    
    # Pour les positions 11-20
    if 11 <= position <= 20:
        return 0.010  # 1.0%
    
    # Pour les positions 21-30
    elif 21 <= position <= 30:
        return 0.005  # 0.5%
    
    # Pour les positions 31-50
    elif 31 <= position <= 50:
        return 0.002  # 0.2%
    
    # Pour les positions 51-100
    elif 51 <= position <= 100:
        return 0.001  # 0.1%
    
    # Pour les positions supérieures à 100 ou non définies
    elif position > 100:
        return 0
    
    # Pour les positions 1-10
    return ctr_data.get(position, 0)
