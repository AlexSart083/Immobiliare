import streamlit as st
from utils import format_currency, format_percentage
from calcoli import calculate_real_estate_investment_improved

def render_header():
    st.title("🏠 Calcolatore Investimenti Immobiliari")
    st.markdown("---")
    st.markdown("### 💡 Analisi Completa con Rivalutazione, Inflazione e Adeguamento Affitti")
    
def render_footer():
    st.markdown("---")
    st.markdown("### ⚠️ **DISCLAIMER IMPORTANTE**")
    st.error("""
**🚨 AVVISO LEGALE - LEGGERE ATTENTAMENTE**
📚 **Scopo Didattico**: Questa applicazione è stata sviluppata esclusivamente a scopo educativo e dimostrativo per illustrare concetti di investimento immobiliare.
🚫 **Non è Consulenza Finanziaria**: I calcoli e le informazioni fornite NON costituiscono consigli di investimento, raccomandazioni immobiliari o consulenza professionale.
⚠️ **Accuratezza dei Dati**: I valori calcolati potrebbero essere imprecisi o non riflettere la complessità del mercato immobiliare reale.
📊 **Responsabilità**: Lo sviluppatore declina ogni responsabilità per decisioni di investimento basate sui risultati ottenuti.
💡 **Raccomandazione**: Consultare SEMPRE un consulente immobiliare e finanziario qualificato prima di investire.
🔒 **Privacy**: I dati inseriti non vengono salvati o trasmessi.
""")
    st.markdown("---")
    st.markdown("### 📝 Note Tecniche:")
    st.info("""
- **Rivalutazione**: Apprezzamento annuo del valore dell'immobile
- **Adeguamento Affitto**: Modalità di aggiornamento del canone nel tempo
- **Valori Nominali**: Senza considerare l'inflazione
- **Valori Reali**: Considerando l'effetto dell'inflazione sul potere d'acquisto
- **CAGR**: Tasso di crescita annuale composto (metrica principale per confronti)
- **ROI**: Return on Investment - rendimento totale sull'investimento iniziale
- **ROE**: Return on Equity - rendimento sul capitale proprio (importante con leverage)
- **Tassa di Proprietà**: Calcolo semplificato basato sul valore dell'immobile (nella realtà dipende dalla rendita catastale)
""")
    st.markdown("---")
    st.markdown("*Sviluppata da **AS** con la collaborazione di **KIM** 🐱 - Versione per fini didattici*")

def display_real_estate_results_simplified(results, params):
    st.success("**🎯 Risultati Analisi Investimento Immobiliare**")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.write("**🏠 Valore Immobile:**")
        st.write(f"• Valore Iniziale: {format_currency(params['valore_immobile'])}")
        st.write(f"• **Valore Finale (Nominale): {format_currency(results['valore_finale_nominale'])}**")
        st.write(f"• **Valore Finale (Reale): {format_currency(results['valore_finale_reale'])}**")
        st.write(f"• Plusvalenza (Nominale): {format_currency(results['guadagno_capitale_nominale'])}")
        rivalutazione_totale = ((results['valore_finale_nominale']/params['valore_immobile'] - 1) * 100) if params['valore_immobile'] > 0 else 0
        st.write(f"• Rivalutazione Totale: {format_percentage(rivalutazione_totale)}")

    with res_col2:
        st.write("**💰 Analisi Affitti:**")
        st.write(f"• Affitto Iniziale: {format_currency(params['affitto_lordo'])}")
        st.write(f"• **Affitto Finale: {format_currency(results['affitto_finale'])}**")
        st.write(f"• **Crescita Affitto Totale: {format_percentage(results['crescita_affitto_totale'])}**")
        st.write(f"• **Totale Affitti Netti (Nominale): {format_currency(results['totale_affitti_netti'])}**")
        st.write(f"• **Totale Affitti Netti (Reale): {format_currency(results['totale_affitti_netti_reale'])}**")
        media_affitti_mensile_reale = results['totale_affitti_netti_reale'] / (12 * params['anni_investimento'])
        st.write(f"• **Media Affitti Mensili Reale: {format_currency(media_affitti_mensile_reale)}**")
        st.write(f"• Modalità Adeguamento: **{params['tipo_adeguamento']}**")

    with res_col3:
        st.write("**📈 Rendimento Totale:**")
        st.write(f"• **Rendimento Totale (Nominale): {format_currency(results['rendimento_totale_nominale'])}**")
        st.write(f"• **Rendimento Totale (Reale): {format_currency(results['rendimento_totale_reale'])}**")
        if results['totale_costi_mutuo'] > 0:
            st.write(f"• **Totale Costi Mutuo: {format_currency(results['totale_costi_mutuo'])}**")
        if results['commissione_iniziale'] > 0 or results['commissione_finale'] > 0:
            st.write(f"• **Commissioni Iniziali: {format_currency(results['commissione_iniziale'])}**")
            st.write(f"• **Commissioni Finali: {format_currency(results['commissione_finale'])}**")
        rendimento_perc_nominale = (results['rendimento_totale_nominale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        rendimento_perc_reale = (results['rendimento_totale_reale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        st.write(f"• Rendimento % (Nominale): {format_percentage(rendimento_perc_nominale)}")

    # Nuova sezione per le metriche di performance
    st.markdown("---")
    st.write("**📊 Metriche di Performance:**")
    
    # Prima riga: CAGR (metrica principale)
    cagr_col1, cagr_col2, cagr_col3 = st.columns(3)
    with cagr_col1:
        st.metric("🏆 CAGR Nominale", f"{format_percentage(results['cagr_nominale'] * 100)}")
        st.caption("✅ Metrica principale per confronti")
    with cagr_col2:
        st.metric("🏆 CAGR Reale", f"{format_percentage(results['cagr_reale'] * 100)}")
        st.caption("✅ Considerando inflazione")
    with cagr_col3:
        st.write("**💡 Perché CAGR?**")
        st.info("Il CAGR normalizza i rendimenti su base annua e permette confronti diretti con altri investimenti")

    # Seconda riga: ROI e ROE
    metrics_col1, metrics_col2 = st.columns(2)
    
    with metrics_col1:
        st.write("**📈 ROI (Return on Investment):**")
        st.write(f"• ROI Totale Nominale: {format_percentage(results['roi_nominale'])}")
        st.write(f"• **ROI Totale Reale: {format_percentage(results['roi_reale'])}**")
        roi_annualizzato = (((1 + results['roi_reale']/100) ** (1/params['anni_investimento'])) - 1) * 100
        st.write(f"• ROI Annualizzato Reale: {format_percentage(roi_annualizzato)}")
        st.write(f"• Investimento Iniziale: {format_currency(results['investimento_iniziale'])}")
        
    with metrics_col2:
        st.write("**🎯 ROE (Return on Equity):**")
        st.write(f"• ROE Totale Nominale: {format_percentage(results['roe_nominale'])}")  
        st.write(f"• **ROE Totale Reale: {format_percentage(results['roe_reale'])}**")
        roe_annualizzato = (((1 + results['roe_reale']/100) ** (1/params['anni_investimento'])) - 1) * 100
        st.write(f"• ROE Annualizzato Reale: {format_percentage(roe_annualizzato)}")
        st.info(results['roe_note'])

    # Analisi mutuo se presente
    if results['totale_costi_mutuo'] > 0:
        st.write("**🏦 Analisi Mutuo:**")
        mortgage_col1, mortgage_col2 = st.columns(2)
        with mortgage_col1:
            st.write(f"• **Totale Costi Mutuo {params['anni_investimento']} anni: {format_currency(results['totale_costi_mutuo'])}**")
            rata_annua = params['rata_mutuo_mensile'] * 12
            percentuale_rata = (rata_annua / params['affitto_lordo']) * 100 if params['affitto_lordo'] > 0 else 0
            st.write(f"• Rata annua vs Affitto iniziale: {format_percentage(percentuale_rata)}")
            if params['anni_restanti_mutuo'] < params['anni_investimento']:
                anni_liberi = params['anni_investimento'] - params['anni_restanti_mutuo']
                st.success(f"✅ Ultimi {anni_liberi} anni senza rata")
        with mortgage_col2:
            if percentuale_rata < 50:
                st.success("✅ Mutuo sostenibile (< 50% affitto)")
            elif percentuale_rata < 70:
                st.warning("⚠️ Mutuo impegnativo (50-70% affitto)")
            else:
                st.error("🚨 Mutuo rischioso (> 70% affitto)")
            rendimento_senza_mutuo = results['rendimento_totale_nominale'] + results['totale_costi_mutuo']
            miglioramento = rendimento_senza_mutuo - results['rendimento_totale_nominale']
            st.info(f"📊 Rendimento senza mutuo: +{format_currency(miglioramento)}")

    st.write("**📋 Riepilogo Investimento:**")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        investimento_totale = params['valore_immobile'] + results['commissione_iniziale'] + - results['commissione_finale']
        capitale_finale_affitti_nominale = results['valore_finale_nominale'] + results['totale_affitti_netti'] - results['commissione_iniziale'] - results['commissione_finale']
        capitale_finale_affitti_reale = results['valore_finale_reale'] + results['totale_affitti_netti_reale'] - results['commissione_iniziale'] - results['commissione_finale']
        st.write(f"• **Capitale Finale + Affitti (Nominale): {format_currency(capitale_finale_affitti_nominale)}**")
        st.write(f"• **Capitale Finale + Affitti (Reale): {format_currency(capitale_finale_affitti_reale)}**")
        if results['commissione_iniziale'] > 0 or results['commissione_finale'] > 0:
            commissioni_totali = results['commissione_iniziale'] + results['commissione_finale']
            st.write(f"• *(Già detratte commissioni totali: {format_currency(commissioni_totali)})*")
    with summary_col2:
        st.info("""
**📝 Nota:** Questo calcolo è basato su assunzioni semplificate. I mercati immobiliari reali sono influenzati da
numerosi fattori non considerati (domanda/offerta locale, normative, condizioni economiche, ecc.).
Consulta sempre un consulente finanziario prima di investire.
""")

def render_real_estate_section():
    st.subheader("🏘️ Analisi Investimento Immobiliare")
    st.info("💡 Stima con rivalutazione, inflazione, mutuo e adeguamento affitti personalizzabile")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**🏠 Parametri Base Immobile**")
        valore_immobile = st.number_input(
            "Valore Immobile (€)", min_value=5000.00, value=200000.00, step=5000.00, key="real_estate_value")
        affitto_lordo = st.number_input(
            "Affitto Lordo Annuo (€)", min_value=0.00, value=12000.00, step=100.00, key="real_estate_rent")
        rivalutazione_annua = st.number_input(
            "Rivalutazione Annua (%)", min_value=0.0, max_value=50.0, value=2.0, step=0.1, key="real_estate_appreciation")
        anni_investimento = st.number_input(
            "Anni di Investimento", min_value=1, value=10, step=1, key="real_estate_years")
        st.write("**Commissioni una tantum**")
        commissione_iniziale = st.number_input(
            "Commissione Iniziale (€)", min_value=0.00, value=0.00, step=100.00, key="real_estate_initial_commission",
            help="Costi di acquisto una tantum (es. agenzia, notaio)")
        commissione_finale = st.number_input(
            "Commissione Finale (€)", min_value=0.00, value=0.00, step=100.00, key="real_estate_final_commission",
            help="Costi di vendita una tantum (es. agenzia)")
    with col2:
        st.write("**💸 Costi e Spese**")
        costi_assicurazione_euro = st.number_input(
            "Costi Assicurazione Annui (€)", min_value=0.00, max_value=10000.00, value=250.00, step=50.00,
            key="real_estate_insurance_euro", help="Costi fissi annui per assicurazione. Verranno adeguati all'inflazione.")
        costi_gestione_euro = st.number_input(
            "Costi Fissi Annui (€)", min_value=0.00, max_value=100000.00, value=250.00, step=50.00,
            key="real_estate_annual_costs_euro", help="Costi fissi annui (es. amministratore, pulizie, piccole manutenzioni). Verranno adeguati all'inflazione.")
        manutenzione_straordinaria_perc = st.number_input(
            "Manutenzione Straordinaria Annua (%)", min_value=0.0, max_value=99.0, value=1.0, step=0.1, key="real_estate_maintenance")
        tassazione_affitti_perc = st.number_input(
            "Tassazione su Affitti (%)", min_value=0.0, max_value=99.0, value=21.0, step=1.0, key="real_estate_tax_rate")
        tassa_catastale_perc = st.number_input(
            "Tassa di proprietà (% valore immobile)", min_value=0.0, max_value=99.0, value=0.8, step=0.1,
            key="real_estate_cadastral_tax",
            help="⚠️ Valore semplificato - Il calcolo della tassa di proprietà in questa applicazione è basato sul **valore dell'immobile**. È importante sapere che per il calcolo ufficiale dell'imposta in Italia è legata alla **rendita catastale** e al **coefficiente catastale** dell'immobile.")
        st.write("**🏦 Mutuo (se presente)**")
        rata_mutuo_mensile = st.number_input(
            "Rata Mutuo Mensile (€)", min_value=0.00, max_value=10000.00, value=0.00, step=50.00, key="real_estate_mortgage_payment")
        anni_restanti_mutuo = st.number_input(
            "Anni Restanti Mutuo", min_value=0, max_value=50, value=0, step=1, key="real_estate_mortgage_years")
    with col3:
        st.write("**📊 Parametri Economici e Adeguamenti**")
        periodo_sfitto_perc = st.number_input(
            "Periodo Annuo Sfitto (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0, key="real_estate_vacancy")
        inflazione_perc = st.number_input(
            "Inflazione Annua (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1, key="real_estate_inflation")
        tipo_adeguamento = st.selectbox(
            "Modalità Adeguamento Affitto", ["Valore Immobile", "Inflazione", "Nessun Adeguamento"], index=0,
            key="real_estate_adjustment_type", help="Scegli come adeguare l'affitto nel tempo")
        adeguamento_affitto_anni = st.number_input(
            "Adeguamento Affitto ogni (Anni)", min_value=1, max_value=99, value=4, step=1,
            key="real_estate_rent_adjustment_years", help="Ogni quanti anni l'affitto viene adeguato secondo la modalità scelta")

        if rata_mutuo_mensile > 0:
            rata_annua_mutuo = rata_mutuo_mensile * 12
            st.info(f"💰 Rata Annua Mutuo: {format_currency(rata_annua_mutuo)}")
            if anni_restanti_mutuo > 0:
                costo_totale_mutuo = rata_annua_mutuo * min(anni_restanti_mutuo, anni_investimento)
                st.info(f"💸 Costo Totale Mutuo nel Periodo: {format_currency(costo_totale_mutuo)}")
        if tipo_adeguamento == "Valore Immobile":
            st.info("🏠 Affitto adeguato al valore rivalutato dell'immobile")
        elif tipo_adeguamento == "Inflazione":
            st.info("📈 Affitto adeguato al tasso di inflazione")
        else:
            st.warning("⚡ Affitto rimane fisso per tutto il periodo")

    st.write("**ℹ️ Note sui Metodi di Adeguamento e Costi:**")
    note_col1, note_col2 = st.columns(2)
    with note_col1:
        st.write("• **Valore Immobile**: L'affitto mantiene la stessa % del valore immobile")
        st.write("• **Inflazione**: L'affitto cresce con l'inflazione")
        st.write("• **Nessun Adeguamento**: Affitto fisso (perdita potere d'acquisto)")
        st.write("• **Costi Gestione**: Importo fisso adeguato annualmente all'inflazione")
        st.write("• **Costi Assicurazione**: Importo fisso adeguato annualmente all'inflazione")
    with note_col2:
        st.write("• Costi percentuali si aggiornano sempre al valore dell'immobile")
        st.write("• Manutenzione e tasse calcolate su valore corrente")
        st.write("• Assicurazione e gestione: costi fissi + inflazione")
        st.write("• **Mutuo**: Se presente, viene considerato fino alla scadenza")
        st.write("• Rate mutuo sono fisse e non si adeguano all'inflazione")

    if st.button("🏠 Calcola Investimento Immobiliare", key="calc_real_estate"):
        try:
            params = {
                'valore_immobile': valore_immobile,
                'affitto_lordo': affitto_lordo,
                'rivalutazione_annua': rivalutazione_annua,
                'anni_investimento': anni_investimento,
                'costi_assicurazione_euro': costi_assicurazione_euro,
                'costi_gestione_euro': costi_gestione_euro,
                'rata_mutuo_mensile': rata_mutuo_mensile,
                'anni_restanti_mutuo': anni_restanti_mutuo,
                'manutenzione_straordinaria_perc': manutenzione_straordinaria_perc,
                'tassazione_affitti_perc': tassazione_affitti_perc,
                'tassa_catastale_perc': tassa_catastale_perc,
                'periodo_sfitto_perc': periodo_sfitto_perc,
                'inflazione_perc': inflazione_perc,
                'adeguamento_affitto_anni': adeguamento_affitto_anni,
                'tipo_adeguamento': tipo_adeguamento,
                'commissione_iniziale': commissione_iniziale,
                'commissione_finale': commissione_finale
            }
            results = calculate_real_estate_investment_improved(params)
            display_real_estate_results_simplified(results, params)
        except Exception as e:
            st.error(f"❌ Errore nel calcolo immobiliare: {str(e)}")
            st.error("Verifica che tutti i valori siano corretti.")
            st.exception(e)
