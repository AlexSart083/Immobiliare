import numpy as np
from scipy.optimize import fsolve
import warnings
from utils import format_currency

def calculate_irr(cash_flows):
    """
    Calcola il TIR (Tasso Interno di Rendimento) / IRR
    
    Args:
        cash_flows: Lista dei flussi di cassa, dove cash_flows[0] è l'investimento iniziale (negativo)
    
    Returns:
        float: TIR come percentuale (es. 0.05 = 5%) o None se non calcolabile
    """
    try:
        # Controlla se ci sono flussi positivi e negativi
        if not any(cf > 0 for cf in cash_flows) or not any(cf < 0 for cf in cash_flows):
            return None
        
        # Funzione NPV da minimizzare
        def npv(rate, cash_flows):
            return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
        
        # Stima iniziale del TIR
        initial_guess = 0.1  # 10%
        
        # Risolvi per trovare il tasso che rende NPV = 0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            irr = fsolve(npv, initial_guess, args=(cash_flows,))[0]
        
        # Verifica che la soluzione sia ragionevole (-100% < IRR < 1000%)
        if -1 < irr < 10:
            return irr
        else:
            return None
            
    except:
        return None

def calculate_irr_for_real_estate(params, affitti_netti_annuali, valore_finale_nominale, valore_finale_reale):
    """
    Calcola il TIR per l'investimento immobiliare considerando i costi reali
    
    Returns:
        dict: TIR nominale e reale
    """
    # Determina l'investimento iniziale reale
    costo_acquisto = params.get('costo_acquisto', 0)
    costo_ristrutturazione = params.get('costo_ristrutturazione', 0)
    
    if costo_acquisto > 0 or costo_ristrutturazione > 0:
        # Usa i costi reali sostenuti
        investimento_iniziale_reale = costo_acquisto + costo_ristrutturazione + params['commissione_iniziale']
    else:
        # Usa il valore dell'immobile come prima
        investimento_iniziale_reale = params['valore_immobile'] + params['commissione_iniziale']
    
    # Flussi di cassa nominali
    cash_flows_nominal = []
    
    # Anno 0: Investimento iniziale (negativo)
    cash_flows_nominal.append(-investimento_iniziale_reale)
    
    # Anni 1 a N-1: Solo affitti netti
    for i in range(len(affitti_netti_annuali) - 1):
        cash_flows_nominal.append(affitti_netti_annuali[i])
    
    # Anno N: Affitti netti + valore finale - commissione finale
    ultimo_flusso = (
        affitti_netti_annuali[-1] + 
        valore_finale_nominale - 
        params['commissione_finale']
    )
    cash_flows_nominal.append(ultimo_flusso)
    
    # Calcola TIR nominale
    tir_nominale = calculate_irr(cash_flows_nominal)
    
    # Flussi di cassa reali (scontati per inflazione)
    cash_flows_real = []
    inflazione_decimal = params['inflazione_perc'] / 100
    
    # Anno 0: Investimento iniziale (stesso valore)
    cash_flows_real.append(-investimento_iniziale_reale)
    
    # Anni 1 a N-1: Affitti netti scontati per inflazione
    for i, affitto_netto in enumerate(affitti_netti_annuali[:-1], 1):
        affitto_reale = affitto_netto / ((1 + inflazione_decimal) ** i)
        cash_flows_real.append(affitto_reale)
    
    # Anno N: Ultimo flusso scontato per inflazione
    ultimo_flusso_reale = (
        affitti_netti_annuali[-1] / ((1 + inflazione_decimal) ** params['anni_investimento']) +
        valore_finale_reale - 
        params['commissione_finale']
    )
    cash_flows_real.append(ultimo_flusso_reale)
    
    # Calcola TIR reale
    tir_reale = calculate_irr(cash_flows_real)
    
    return {
        'tir_nominale': tir_nominale * 100 if tir_nominale is not None else None,
        'tir_reale': tir_reale * 100 if tir_reale is not None else None,
        'cash_flows_nominal': cash_flows_nominal,
        'cash_flows_real': cash_flows_real,
        'investimento_iniziale_reale': investimento_iniziale_reale
    }

def calculate_roi_roe_metrics(params, rendimento_totale_nominale, rendimento_totale_reale):
    """
    Calcola ROI e ROE per l'investimento immobiliare considerando i costi reali
    ROI = rendimento sull'investimento totale (senza considerare il finanziamento)
    ROE = rendimento sul capitale proprio (considerando il leverage del mutuo)
    """
    # Determina l'investimento iniziale reale
    costo_acquisto = params.get('costo_acquisto', 0)
    costo_ristrutturazione = params.get('costo_ristrutturazione', 0)
    
    if costo_acquisto > 0 or costo_ristrutturazione > 0:
        # Usa i costi reali sostenuti
        investimento_iniziale = costo_acquisto + costo_ristrutturazione + params['commissione_iniziale']
    else:
        # Usa il valore dell'immobile come prima
        investimento_iniziale = params['valore_immobile'] + params['commissione_iniziale']
    
    if params['rata_mutuo_mensile'] > 0:
        # CON MUTUO: ROI e ROE sono diversi
        
        # ROI: Rendimento come se avessi pagato tutto cash (senza costi mutuo)
        # Aggiungiamo i costi del mutuo al rendimento per calcolare il ROI "puro"
        anni_con_mutuo = min(params['anni_restanti_mutuo'], params['anni_investimento'])
        costi_mutuo_totali = params['rata_mutuo_mensile'] * 12 * anni_con_mutuo
        
        rendimento_senza_mutuo_nominale = rendimento_totale_nominale + costi_mutuo_totali
        rendimento_senza_mutuo_reale = rendimento_totale_reale + costi_mutuo_totali
        
        roi_nominale = (rendimento_senza_mutuo_nominale / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
        roi_reale = (rendimento_senza_mutuo_reale / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
        
        # ROE: Rendimento sul capitale proprio (con i costi del mutuo)
        # Assumiamo che il capitale proprio sia l'investimento iniziale 
        # (nella realtà dovremmo sapere quanto del valore immobile è coperto dal mutuo)
        capitale_proprio = investimento_iniziale
        roe_nominale = (rendimento_totale_nominale / capitale_proprio) * 100 if capitale_proprio > 0 else 0
        roe_reale = (rendimento_totale_reale / capitale_proprio) * 100 if capitale_proprio > 0 else 0
        
        roe_note = f"⚠️ ROE calcolato su capitale proprio stimato di {format_currency(capitale_proprio)}. Per calcolo preciso specificare l'importo del mutuo iniziale."
        
    else:
        # SENZA MUTUO: ROI = ROE
        roi_nominale = (rendimento_totale_nominale / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
        roi_reale = (rendimento_totale_reale / investimento_iniziale) * 100 if investimento_iniziale > 0 else 0
        
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

def calculate_real_estate_investment_improved(params):
    rivalutazione_decimal = params['rivalutazione_annua'] / 100
    inflazione_decimal = params['inflazione_perc'] / 100
    periodo_sfitto_decimal = params['periodo_sfitto_perc'] / 100
    manutenzione_decimal = params['manutenzione_straordinaria_perc'] / 100
    tassazione_decimal = params['tassazione_affitti_perc'] / 100
    tassa_catastale_decimal = params['tassa_catastale_perc'] / 100

    valore_corrente = params['valore_immobile']
    affitto_corrente = params['affitto_lordo']
    costi_gestione_correnti = params['costi_gestione_euro']
    costi_assicurazione_correnti = params['costi_assicurazione_euro']
    rapporto_affitto_iniziale = params['affitto_lordo'] / params['valore_immobile']

    rata_mutuo_annua = params['rata_mutuo_mensile'] * 12 if params['rata_mutuo_mensile'] > 0 else 0

    # NUOVO: Calcola plus/minusvalore iniziale
    costo_acquisto = params.get('costo_acquisto', 0)
    costo_ristrutturazione = params.get('costo_ristrutturazione', 0)
    plusvalore_minusvalore_iniziale = 0
    
    if costo_acquisto > 0 or costo_ristrutturazione > 0:
        costo_totale_sostenuto = costo_acquisto + costo_ristrutturazione
        plusvalore_minusvalore_iniziale = params['valore_immobile'] - costo_totale_sostenuto
    
    # Determina l'investimento iniziale reale per CAGR
    if costo_acquisto > 0 or costo_ristrutturazione > 0:
        investimento_iniziale_totale = costo_acquisto + costo_ristrutturazione + params['commissione_iniziale']
    else:
        investimento_iniziale_totale = params['valore_immobile'] + params['commissione_iniziale']

    valori_annuali = []
    affitti_lordi_annuali = []
    affitti_netti_annuali = []
    rendimenti_annuali = []
    costi_gestione_annuali = []
    costi_mutuo_annuali = []

    for anno in range(1, params['anni_investimento'] + 1):
        valore_corrente = valore_corrente * (1 + rivalutazione_decimal)
        costi_gestione_correnti = costi_gestione_correnti * (1 + inflazione_decimal)
        costi_assicurazione_correnti = costi_assicurazione_correnti * (1 + inflazione_decimal)
        adeguamento_questo_anno = (anno % params['adeguamento_affitto_anni'] == 0)

        if adeguamento_questo_anno:
            if params['tipo_adeguamento'] == "Valore Immobile":
                affitto_corrente = valore_corrente * rapporto_affitto_iniziale
            elif params['tipo_adeguamento'] == "Inflazione":
                inflazione_cumulativa = (1 + inflazione_decimal) ** params['adeguamento_affitto_anni']
                affitto_corrente = affitto_corrente * inflazione_cumulativa
            # Nessun Adeguamento: affitto_corrente invariato

        costo_mutuo_anno = 0
        if rata_mutuo_annua > 0 and anno <= params['anni_restanti_mutuo']:
            costo_mutuo_anno = rata_mutuo_annua

        tassa_catastale_corrente = valore_corrente * tassa_catastale_decimal
        affitto_effettivo = affitto_corrente * (1 - periodo_sfitto_decimal)
        tasse_affitto = affitto_effettivo * tassazione_decimal
        manutenzione_annua = valore_corrente * manutenzione_decimal

        costi_totali_annui = (
            costi_assicurazione_correnti
            + costi_gestione_correnti
            + manutenzione_annua
            + tassa_catastale_corrente
            + tasse_affitto
            + costo_mutuo_anno
        )
        affitto_netto = affitto_effettivo - costi_totali_annui
        rendimento_annuo = (affitto_netto / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0

        valori_annuali.append(valore_corrente)
        affitti_lordi_annuali.append(affitto_corrente)
        affitti_netti_annuali.append(affitto_netto)
        rendimenti_annuali.append(rendimento_annuo)
        costi_gestione_annuali.append(costi_gestione_correnti)
        costi_mutuo_annuali.append(costo_mutuo_anno)

    valore_finale_nominale = valori_annuali[-1]
    valore_finale_reale = valore_finale_nominale / ((1 + inflazione_decimal) ** params['anni_investimento'])
    totale_affitti_netti = sum(affitti_netti_annuali)
    totale_costi_mutuo = sum(costi_mutuo_annuali)
    rendimento_medio_annuo = sum(rendimenti_annuali) / len(rendimenti_annuali) if rendimenti_annuali else 0

    guadagno_capitale_nominale = valore_finale_nominale - params['valore_immobile']
    guadagno_capitale_reale = valore_finale_reale - params['valore_immobile']

    totale_affitti_netti_reale = 0
    for anno, affitto_netto_anno in enumerate(affitti_netti_annuali, 1):
        valore_presente_affitto = affitto_netto_anno / ((1 + inflazione_decimal) ** anno)
        totale_affitti_netti_reale += valore_presente_affitto

    # MODIFICATO: Aggiungi plus/minusvalore iniziale al rendimento
    rendimento_totale_nominale = (
        totale_affitti_netti + guadagno_capitale_nominale + plusvalore_minusvalore_iniziale
        - params['commissione_iniziale'] - params['commissione_finale']
    )
    rendimento_totale_reale = (
        totale_affitti_netti_reale + guadagno_capitale_reale + plusvalore_minusvalore_iniziale
        - params['commissione_iniziale'] - params['commissione_finale']
    )

    # Valore finale totale (quello che ottieni)
    valore_finale_totale_nominale = valore_finale_nominale + totale_affitti_netti - params['commissione_finale']
    valore_finale_totale_reale = valore_finale_reale + totale_affitti_netti_reale - params['commissione_finale']

    # CAGR CORRETTO con investimento iniziale reale
    cagr_nominale = (
        (valore_finale_totale_nominale / investimento_iniziale_totale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale_totale > 0 else 0

    cagr_reale = (
        (valore_finale_totale_reale / investimento_iniziale_totale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale_totale > 0 else 0

    affitto_iniziale = params['affitto_lordo']
    affitto_finale = affitti_lordi_annuali[-1]
    crescita_affitto_totale = ((affitto_finale / affitto_iniziale) - 1) * 100 if affitto_iniziale > 0 else 0
    crescita_affitto_annua = (
        ((affitto_finale / affitto_iniziale) ** (1 / params['anni_investimento']) - 1) * 100
        if affitto_iniziale > 0 and params['anni_investimento'] > 0 else 0
    )

    costi_gestione_finali = costi_gestione_annuali[-1]
    crescita_costi_gestione = ((costi_gestione_finali / params['costi_gestione_euro']) - 1) * 100 \
        if params['costi_gestione_euro'] > 0 else 0

    # Calcola ROI e ROE con i nuovi parametri
    roi_roe_metrics = calculate_roi_roe_metrics(params, rendimento_totale_nominale, rendimento_totale_reale)

    # Calcola TIR/IRR con i nuovi parametri
    tir_metrics = calculate_irr_for_real_estate(params, affitti_netti_annuali, valore_finale_nominale, valore_finale_reale)

    return {
        'valori_annuali': valori_annuali,
        'affitti_lordi_annuali': affitti_lordi_annuali,
        'affitti_netti_annuali': affitti_netti_annuali,
        'rendimenti_annuali': rendimenti_annuali,
        'costi_gestione_annuali': costi_gestione_annuali,
        'costi_mutuo_annuali': costi_mutuo_annuali,
        'valore_finale_nominale': valore_finale_nominale,
        'valore_finale_reale': valore_finale_reale,
        'totale_affitti_netti': totale_affitti_netti,
        'totale_affitti_netti_reale': totale_affitti_netti_reale,
        'totale_costi_mutuo': totale_costi_mutuo,
        'rendimento_medio_annuo': rendimento_medio_annuo,
        'guadagno_capitale_nominale': guadagno_capitale_nominale,
        'guadagno_capitale_reale': guadagno_capitale_reale,
        'rendimento_totale_nominale': rendimento_totale_nominale,
        'rendimento_totale_reale': rendimento_totale_reale,
        'cagr_nominale': cagr_nominale,
        'cagr_reale': cagr_reale,
        'affitto_finale': affitto_finale,
        'crescita_affitto_totale': crescita_affitto_totale,
        'crescita_affitto_annua': crescita_affitto_annua,
        'costi_gestione_finali': costi_gestione_finali,
        'crescita_costi_gestione': crescita_costi_gestione,
        'commissione_iniziale': params['commissione_iniziale'],
        'commissione_finale': params['commissione_finale'],
        # NUOVO: Plus/minusvalore iniziale
        'plusvalore_minusvalore_iniziale': plusvalore_minusvalore_iniziale,
        'costo_acquisto': costo_acquisto,
        'costo_ristrutturazione': costo_ristrutturazione,
        'investimento_iniziale_reale': investimento_iniziale_totale,
        # ROI e ROE
        'roi_nominale': roi_roe_metrics['roi_nominale'],
        'roi_reale': roi_roe_metrics['roi_reale'],
        'roe_nominale': roi_roe_metrics['roe_nominale'],
        'roe_reale': roi_roe_metrics['roe_reale'],
        'roe_note': roi_roe_metrics['roe_note'],
        'investimento_iniziale': roi_roe_metrics['investimento_iniziale'],
        # TIR/IRR
        'tir_nominale': tir_metrics['tir_nominale'],
        'tir_reale': tir_metrics['tir_reale'],
        'cash_flows_nominal': tir_metrics['cash_flows_nominal'],
        'cash_flows_real': tir_metrics['cash_flows_real']
    }
