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

    valori_annuali = []
    affitti_lordi_annuali = []
    affitti_netti_annuali = []
    affitti_netti_senza_mutuo_annuali = []
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

        # Costi senza mutuo
        costi_senza_mutuo = (
            costi_assicurazione_correnti
            + costi_gestione_correnti
            + manutenzione_annua
            + tassa_catastale_corrente
            + tasse_affitto
        )
        
        # Costi totali con mutuo
        costi_totali_annui = costi_senza_mutuo + costo_mutuo_anno
        
        # Affitti netti
        affitto_netto = affitto_effettivo - costi_totali_annui
        affitto_netto_senza_mutuo = affitto_effettivo - costi_senza_mutuo
        
        rendimento_annuo = (affitto_netto / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0

        valori_annuali.append(valore_corrente)
        affitti_lordi_annuali.append(affitto_corrente)
        affitti_netti_annuali.append(affitto_netto)
        affitti_netti_senza_mutuo_annuali.append(affitto_netto_senza_mutuo)
        rendimenti_annuali.append(rendimento_annuo)
        costi_gestione_annuali.append(costi_gestione_correnti)
        costi_mutuo_annuali.append(costo_mutuo_anno)

    # Calcoli finali
    valore_finale_nominale = valori_annuali[-1]
    valore_finale_reale = valore_finale_nominale / ((1 + inflazione_decimal) ** params['anni_investimento'])
    totale_affitti_netti = sum(affitti_netti_annuali)
    totale_affitti_netti_senza_mutuo = sum(affitti_netti_senza_mutuo_annuali)
    totale_costi_mutuo = sum(costi_mutuo_annuali)
    rendimento_medio_annuo = sum(rendimenti_annuali) / len(rendimenti_annuali) if rendimenti_annuali else 0

    guadagno_capitale_nominale = valore_finale_nominale - params['valore_immobile']
    guadagno_capitale_reale = valore_finale_reale - params['valore_immobile']

    # Calcolo valore presente degli affitti (reale)
    totale_affitti_netti_reale = 0
    totale_affitti_netti_senza_mutuo_reale = 0
    
    for anno, (affitto_netto_anno, affitto_senza_mutuo_anno) in enumerate(zip(affitti_netti_annuali, affitti_netti_senza_mutuo_annuali), 1):
        # Fattore di sconto per il valore presente
        fattore_sconto = (1 + inflazione_decimal) ** anno
        
        # Valore presente dell'affitto netto (con mutuo)
        valore_presente_affitto = affitto_netto_anno / fattore_sconto
        totale_affitti_netti_reale += valore_presente_affitto
        
        # Valore presente dell'affitto netto senza mutuo
        valore_presente_senza_mutuo = affitto_senza_mutuo_anno / fattore_sconto
        totale_affitti_netti_senza_mutuo_reale += valore_presente_senza_mutuo

    # Rendimenti totali
    rendimento_totale_nominale = (
        totale_affitti_netti + guadagno_capitale_nominale
        - params['commissione_iniziale'] - params['commissione_finale']
    )
    rendimento_totale_reale = (
        totale_affitti_netti_reale + guadagno_capitale_reale
        - params['commissione_iniziale'] - params['commissione_finale']
    )

    # Rendimenti totali senza mutuo
    rendimento_totale_senza_mutuo_nominale = (
        totale_affitti_netti_senza_mutuo + guadagno_capitale_nominale
        - params['commissione_iniziale'] - params['commissione_finale']
    )
    rendimento_totale_senza_mutuo_reale = (
        totale_affitti_netti_senza_mutuo_reale + guadagno_capitale_reale
        - params['commissione_iniziale'] - params['commissione_finale']
    )

    # CAGR calculations
    investimento_iniziale = params['valore_immobile']
    capitale_finale_nominale = valore_finale_nominale + totale_affitti_netti - params['commissione_iniziale'] - params['commissione_finale']
    capitale_finale_reale = valore_finale_reale + totale_affitti_netti_reale - params['commissione_iniziale'] - params['commissione_finale']
    
    cagr_nominale = (
        (capitale_finale_nominale / investimento_iniziale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale > 0 and capitale_finale_nominale > 0 else 0

    cagr_reale = (
        (capitale_finale_reale / investimento_iniziale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale > 0 and capitale_finale_reale > 0 else 0

    # CAGR senza mutuo
    capitale_finale_senza_mutuo_nominale = valore_finale_nominale + totale_affitti_netti_senza_mutuo - params['commissione_iniziale'] - params['commissione_finale']
    capitale_finale_senza_mutuo_reale = valore_finale_reale + totale_affitti_netti_senza_mutuo_reale - params['commissione_iniziale'] - params['commissione_finale']
    
    cagr_senza_mutuo_nominale = (
        (capitale_finale_senza_mutuo_nominale / investimento_iniziale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale > 0 and capitale_finale_senza_mutuo_nominale > 0 else 0

    cagr_senza_mutuo_reale = (
        (capitale_finale_senza_mutuo_reale / investimento_iniziale) ** (1 / params['anni_investimento']) - 1
    ) if investimento_iniziale > 0 and capitale_finale_senza_mutuo_reale > 0 else 0

    # Analisi crescita affitti
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

    return {
        'valori_annuali': valori_annuali,
        'affitti_lordi_annuali': affitti_lordi_annuali,
        'affitti_netti_annuali': affitti_netti_annuali,
        'affitti_netti_senza_mutuo_annuali': affitti_netti_senza_mutuo_annuali,
        'rendimenti_annuali': rendimenti_annuali,
        'costi_gestione_annuali': costi_gestione_annuali,
        'costi_mutuo_annuali': costi_mutuo_annuali,
        'valore_finale_nominale': valore_finale_nominale,
        'valore_finale_reale': valore_finale_reale,
        'totale_affitti_netti': totale_affitti_netti,
        'totale_affitti_netti_reale': totale_affitti_netti_reale,
        'totale_affitti_netti_senza_mutuo': totale_affitti_netti_senza_mutuo,
        'totale_affitti_netti_senza_mutuo_reale': totale_affitti_netti_senza_mutuo_reale,
        'totale_costi_mutuo': totale_costi_mutuo,
        'rendimento_medio_annuo': rendimento_medio_annuo,
        'guadagno_capitale_nominale': guadagno_capitale_nominale,
        'guadagno_capitale_reale': guadagno_capitale_reale,
        'rendimento_totale_nominale': rendimento_totale_nominale,
        'rendimento_totale_reale': rendimento_totale_reale,
        'rendimento_totale_senza_mutuo_nominale': rendimento_totale_senza_mutuo_nominale,
        'rendimento_totale_senza_mutuo_reale': rendimento_totale_senza_mutuo_reale,
        'cagr_nominale': cagr_nominale,
        'cagr_reale': cagr_reale,
        'cagr_senza_mutuo_nominale': cagr_senza_mutuo_nominale,
        'cagr_senza_mutuo_reale': cagr_senza_mutuo_reale,
        'affitto_finale': affitto_finale,
        'crescita_affitto_totale': crescita_affitto_totale,
        'crescita_affitto_annua': crescita_affitto_annua,
        'costi_gestione_finali': costi_gestione_finali,
        'crescita_costi_gestione': crescita_costi_gestione,
        'commissione_iniziale': params['commissione_iniziale'],
        'commissione_finale': params['commissione_finale']
    }
