# Aggiungi queste funzioni in calcoli.py

def calculate_roi_roe_metrics(params, results):
    """
    Calcola ROI e ROE per l'investimento immobiliare
    """
    # Investimento iniziale totale
    investimento_iniziale = params['valore_immobile'] + params['commissione_iniziale']
    
    # ROI Nominale e Reale
    roi_nominale = (results['rendimento_totale_nominale'] / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
    roi_reale = (results['rendimento_totale_reale'] / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
    
    # Calcolo ROE (considerando il leverage del mutuo)
    if params['rata_mutuo_mensile'] > 0:
        # Con mutuo: capitale proprio = valore immobile - importo mutuo residuo
        # Semplifichiamo assumendo che il mutuo copra una % del valore immobile
        # In una versione più avanzata, dovresti chiedere l'importo del mutuo iniziale
        
        # Per ora, stimiamo il capitale proprio come investimento iniziale
        # (assumendo che l'utente abbia versato la differenza tra valore e mutuo)
        capitale_proprio = investimento_iniziale
        roe_nominale = roi_nominale  # Se non conosciamo l'importo del mutuo, ROE = ROI
        roe_reale = roi_reale
        
        # Nota: per un calcolo ROE preciso servirebbe l'importo del mutuo iniziale
        roe_note = "⚠️ Per ROE preciso specificare importo mutuo iniziale"
    else:
        # Senza mutuo: ROE = ROI
        capitale_proprio = investimento_iniziale
        roe_nominale = roi_nominale
        roe_reale = roi_reale
        roe_note = "✅ Senza leverage: ROE = ROI"
    
    return {
        'roi_nominale': roi_nominale,
        'roi_reale': roi_reale,
        'roe_nominale': roe_nominale,
        'roe_reale': roe_reale,
        'roe_note': roe_note,
        'investimento_iniziale': investimento_iniziale,
        'capitale_proprio': capitale_proprio
    }

# Modifica nella funzione calculate_real_estate_investment_improved
# Aggiungi alla fine, prima del return:

    # Calcola ROI e ROE
    roi_roe_metrics = calculate_roi_roe_metrics(params, {
        'rendimento_totale_nominale': rendimento_totale_nominale,
        'rendimento_totale_reale': rendimento_totale_reale
    })
    
    # Aggiungi i nuovi valori al return
    result = {
        # ... tutti i valori esistenti ...
        'roi_nominale': roi_roe_metrics['roi_nominale'],
        'roi_reale': roi_roe_metrics['roi_reale'], 
        'roe_nominale': roi_roe_metrics['roe_nominale'],
        'roe_reale': roi_roe_metrics['roe_reale'],
        'roe_note': roi_roe_metrics['roe_note'],
        'investimento_iniziale': roi_roe_metrics['investimento_iniziale']
    }
