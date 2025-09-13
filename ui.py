import streamlit as st
from utils import format_currency, format_percentage
from calcoli import calculate_real_estate_investment_improved
from i18n import get_text, render_language_selector

def render_header():
    # Selettore lingua in alto
    render_language_selector()
    
    st.title(get_text('app_title'))
    st.markdown("---")
    st.markdown(f"### {get_text('app_subtitle')}")
    
def render_footer():
    st.markdown("---")
    st.markdown(f"### {get_text('disclaimer_title')}")
    st.error(f"""
{get_text('legal_notice')}
📚 {get_text('educational_purpose')}
🚫 {get_text('not_financial_advice')}
⚠️ {get_text('data_accuracy')}
📊 {get_text('responsibility')}
💡 {get_text('recommendation')}
🔒 {get_text('privacy')}
""")
    st.markdown("---")
    st.markdown(f"### {get_text('technical_notes')}")
    st.info(f"""
{get_text('appreciation_note')}
{get_text('rent_adjustment_note')}
{get_text('nominal_values_note')}
{get_text('real_values_note')}
- **CAGR**: {get_text('cagr_note')}
- **TIR**: {get_text('tir_note')}
- **ROI**: {get_text('roi_note')}
- **ROE**: {get_text('roe_note')}
{get_text('property_tax_note')}
""")
    st.markdown("---")
    st.markdown(f"*{get_text('developed_by')}*")

def display_real_estate_results_simplified(results, params):
    st.success(f"**{get_text('results_title')}**")

    # Analisi dell'affare fatto
    if params.get('costo_acquisto', 0) > 0 or params.get('costo_ristrutturazione', 0) > 0:
        st.markdown("---")
        st.write("**💰 Analisi dell'Investimento Iniziale:**")
        
        costo_totale_sostenuto = params.get('costo_acquisto', 0) + params.get('costo_ristrutturazione', 0)
        differenza_valore = params['valore_immobile'] - costo_totale_sostenuto
        
        col_deal1, col_deal2, col_deal3 = st.columns(3)
        
        with col_deal1:
            st.write(f"• Costo Acquisto: {format_currency(params.get('costo_acquisto', 0))}")
            st.write(f"• Costo Ristrutturazione: {format_currency(params.get('costo_ristrutturazione', 0))}")
            st.write(f"• **Totale Investito: {format_currency(costo_totale_sostenuto)}**")
            
        with col_deal2:
            st.write(f"• Valore Immobile Attuale: {format_currency(params['valore_immobile'])}")
            if differenza_valore > 0:
                st.success(f"• **Plusvalore Iniziale: +{format_currency(differenza_valore)}** ✅")
                percentuale_guadagno = (differenza_valore / costo_totale_sostenuto) * 100 if costo_totale_sostenuto > 0 else 0
                st.success(f"• **Ottimo affare! +{format_percentage(percentuale_guadagno)}** 🎯")
            elif differenza_valore < 0:
                st.error(f"• **Minusvalore Iniziale: {format_currency(differenza_valore)}** ⚠️")
                percentuale_perdita = (abs(differenza_valore) / costo_totale_sostenuto) * 100 if costo_totale_sostenuto > 0 else 0
                st.error(f"• **Affare svantaggioso: -{format_percentage(percentuale_perdita)}** 📉")
            else:
                st.info("• **Valore in pari** ⚖️")
                
        with col_deal3:
            if 'plusvalore_minusvalore_iniziale' in results:
                st.write("• **Impatto sui Calcoli:**")
                if results['plusvalore_minusvalore_iniziale'] > 0:
                    st.success(f"• Aggiunto al rendimento: +{format_currency(results['plusvalore_minusvalore_iniziale'])}")
                elif results['plusvalore_minusvalore_iniziale'] < 0:
                    st.error(f"• Sottratto dal rendimento: {format_currency(results['plusvalore_minusvalore_iniziale'])}")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.write(f"**{get_text('property_value_section')}**")
        st.write(f"{get_text('initial_value')}{format_currency(params['valore_immobile'])}")
        st.write(f"{get_text('final_nominal_value')}{format_currency(results['valore_finale_nominale'])}**")
        st.write(f"{get_text('final_real_value')}{format_currency(results['valore_finale_reale'])}**")
        st.write(f"{get_text('capital_gain_nominal')}{format_currency(results['guadagno_capitale_nominale'])}")
        rivalutazione_totale = ((results['valore_finale_nominale']/params['valore_immobile'] - 1) * 100) if params['valore_immobile'] > 0 else 0
        st.write(f"{get_text('total_appreciation')}{format_percentage(rivalutazione_totale)}")

    with res_col2:
        st.write(f"**{get_text('rent_analysis')}**")
        
        # Affitto mensile iniziale e finale
        affitto_mensile_iniziale = params['affitto_lordo'] / 12
        affitto_mensile_finale = results['affitto_finale'] / 12
        
        st.write(f"{get_text('initial_monthly_rent')}{format_currency(affitto_mensile_iniziale)}")
        st.write(f"{get_text('initial_rent')}{format_currency(params['affitto_lordo'])}")
        st.write(f"{get_text('final_monthly_rent')}{format_currency(affitto_mensile_finale)}**")
        st.write(f"{get_text('final_rent')}{format_currency(results['affitto_finale'])}**")
        st.write(f"{get_text('total_rent_growth')}{format_percentage(results['crescita_affitto_totale'])}**")
        st.write(f"{get_text('total_net_rents_nominal')}{format_currency(results['totale_affitti_netti'])}**")
        st.write(f"{get_text('total_net_rents_real')}{format_currency(results['totale_affitti_netti_reale'])}**")
        media_affitti_mensile_reale = results['totale_affitti_netti_reale'] / (12 * params['anni_investimento'])
        st.write(f"{get_text('average_monthly_real')}{format_currency(media_affitti_mensile_reale)}**")
        st.write(f"{get_text('adjustment_mode')}{params['tipo_adeguamento']}**")

    with res_col3:
        st.write(f"**{get_text('total_return')}**")
        st.write(f"{get_text('total_return_nominal')}{format_currency(results['rendimento_totale_nominale'])}**")
        st.write(f"{get_text('total_return_real')}{format_currency(results['rendimento_totale_reale'])}**")
        if results['totale_costi_mutuo'] > 0:
            st.write(f"{get_text('total_mortgage_costs')}{format_currency(results['totale_costi_mutuo'])}**")
        if results['commissione_iniziale'] > 0 or results['commissione_finale'] > 0:
            st.write(f"{get_text('initial_commissions')}{format_currency(results['commissione_iniziale'])}**")
            st.write(f"{get_text('final_commissions')}{format_currency(results['commissione_finale'])}**")
        rendimento_perc_nominale = (results['rendimento_totale_nominale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        rendimento_perc_reale = (results['rendimento_totale_reale'] / params['valore_immobile']) * 100 if params['valore_immobile'] > 0 else 0
        st.write(f"{get_text('return_perc_nominal')}{format_percentage(rendimento_perc_nominale)}")

    # Nuova sezione per le metriche di performance
    st.markdown("---")
    st.write("**📊 Metriche di Performance:**")
    
    # Prima riga: CAGR e TIR (metriche principali)
    main_metrics_col1, main_metrics_col2, main_metrics_col3, main_metrics_col4 = st.columns(4)
    
    with main_metrics_col1:
        st.metric("🏆 CAGR Nominale", f"{format_percentage(results['cagr_nominale'] * 100)}")
        st.caption("✅ Crescita annuale composta")
    
    with main_metrics_col2:
        st.metric("🏆 CAGR Reale", f"{format_percentage(results['cagr_reale'] * 100)}")
        st.caption("✅ Considerando inflazione")
    
    with main_metrics_col3:
        if results.get('tir_nominale') is not None:
            st.metric("🎯 TIR Nominale", f"{format_percentage(results['tir_nominale'])}")
            st.caption("✅ Tasso interno rendimento")
        else:
            st.metric("🎯 TIR Nominale", "N/A")
            st.caption("⚠️ Calcolo non possibile")
    
    with main_metrics_col4:
        if results.get('tir_reale') is not None:
            st.metric("🎯 TIR Reale", f"{format_percentage(results['tir_reale'])}")
            st.caption("✅ TIR deflazionato")
        else:
            st.metric("🎯 TIR Reale", "N/A")
            st.caption("⚠️ Calcolo non possibile")

    # Spiegazione delle metriche principali
    st.info("""
    **💡 Metriche Principali:**
    - **CAGR**: Tasso di crescita annuale composto - normalizza i rendimenti e permette confronti diretti
    - **TIR**: Tasso Interno di Rendimento - considera il timing dei flussi di cassa e è lo standard nel settore immobiliare
    - Entrambe sono ottime per confrontare con altri investimenti
    """)

    # Seconda riga: ROI e ROE (metriche secondarie)
    st.markdown("### 📈 Metriche Secondarie:")
    secondary_col1, secondary_col2 = st.columns(2)
    
    with secondary_col1:
        st.write("**📊 ROI (Return on Investment):**")
        st.write(f"• ROI Totale Nominale: {format_percentage(results['roi_nominale'])}")
        st.write(f"• **ROI Totale Reale: {format_percentage(results['roi_reale'])}**")
        roi_annualizzato = (((1 + results['roi_nominale']/100) ** (1/params['anni_investimento'])) - 1) * 100
        st.write(f"• ROI Annualizzato Nominale: {format_percentage(roi_annualizzato)}")
        st.write(f"• Investimento Iniziale: {format_currency(results['investimento_iniziale'])}")
        
    with secondary_col2:
        st.write("**🎯 ROE (Return on Equity):**")
        st.write(f"• ROE Totale Nominale: {format_percentage(results['roe_nominale'])}")  
        st.write(f"• **ROE Totale Reale: {format_percentage(results['roe_reale'])}**")
        roe_annualizzato = (((1 + results['roe_nominale']/100) ** (1/params['anni_investimento'])) - 1) * 100
        st.write(f"• ROE Annualizzato Nominale: {format_percentage(roe_annualizzato)}")
        st.info(results['roe_note'])

    # Confronto metriche se TIR è disponibile
    if results.get('tir_nominale') is not None and results.get('tir_reale') is not None:
        st.markdown("### 🔍 Confronto Metriche:")
        comparison_col1, comparison_col2 = st.columns(2)
        
        with comparison_col1:
            st.write("**📊 Valori Nominali:**")
            metrics_comparison = [
                ("CAGR", results['cagr_nominale'] * 100),
                ("TIR", results['tir_nominale']),
                ("ROI Annualizzato", roi_annualizzato)
            ]
            metrics_comparison.sort(key=lambda x: x[1], reverse=True)
            
            for i, (metric, value) in enumerate(metrics_comparison):
                icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.write(f"{icon} {metric}: {format_percentage(value)}")
        
        with comparison_col2:
            st.write("**📊 Valori Reali:**")
            real_metrics_comparison = [
                ("CAGR", results['cagr_reale'] * 100),
                ("TIR", results['tir_reale']),
                ("ROI", results['roi_reale'])
            ]
            real_metrics_comparison.sort(key=lambda x: x[1], reverse=True)
            
            for i, (metric, value) in enumerate(real_metrics_comparison):
                icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.write(f"{icon} {metric}: {format_percentage(value)}")

        # Analisi delle differenze
        cagr_tir_diff = abs(results['cagr_nominale'] * 100 - results['tir_nominale'])
        if cagr_tir_diff < 0.5:
            st.success("✅ CAGR e TIR sono molto simili - flussi di cassa ben distribuiti nel tempo")
        elif cagr_tir_diff < 2:
            st.info("ℹ️ Piccola differenza tra CAGR e TIR - normale per investimenti immobiliari")
        else:
            st.warning("⚠️ Differenza significativa tra CAGR e TIR - analizzare la distribuzione dei flussi di cassa")

    # Analisi mutuo se presente
    if results['totale_costi_mutuo'] > 0:
        st.markdown("---")
        st.write(f"**{get_text('mortgage_analysis')}**")
        mortgage_col1, mortgage_col2 = st.columns(2)
        with mortgage_col1:
            st.write(f"{get_text('total_mortgage_costs_years')}{params['anni_investimento']}{get_text('years_suffix')}{format_currency(results['totale_costi_mutuo'])}**")
            
            # Confronti sia mensili che annuali
            affitto_mensile_iniziale = params['affitto_lordo'] / 12
            percentuale_rata_mensile = (params['rata_mutuo_mensile'] / affitto_mensile_iniziale) * 100 if affitto_mensile_iniziale > 0 else 0
            st.write(f"{get_text('monthly_payment_vs_initial_rent')}{format_percentage(percentuale_rata_mensile)}")
            
            rata_annua = params['rata_mutuo_mensile'] * 12
            percentuale_rata_annua = (rata_annua / params['affitto_lordo']) * 100 if params['affitto_lordo'] > 0 else 0
            st.write(f"{get_text('annual_vs_initial_rent')}{format_percentage(percentuale_rata_annua)}")
            
            if params['anni_restanti_mutuo'] < params['anni_investimento']:
                anni_liberi = params['anni_investimento'] - params['anni_restanti_mutuo']
                st.success(f"✅ {get_text('mortgage_free_years')}{anni_liberi}{get_text('years_without_payment')}")
                
        with mortgage_col2:
            # Usa percentuale mensile per la valutazione
            if percentuale_rata_mensile < 50:
                st.success(get_text('sustainable_mortgage_monthly'))
            elif percentuale_rata_mensile < 70:
                st.warning(get_text('challenging_mortgage_monthly'))
            else:
                st.error(get_text('risky_mortgage_monthly'))
            
            rendimento_senza_mutuo = results['rendimento_totale_nominale'] + results['totale_costi_mutuo']
            miglioramento = rendimento_senza_mutuo - results['rendimento_totale_nominale']
            st.info(f"{get_text('return_without_mortgage')}{format_currency(miglioramento)}")

    st.markdown("---")
    st.write(f"**{get_text('investment_summary')}**")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        investimento_totale = params['valore_immobile'] + results['commissione_iniziale'] + - results['commissione_finale']
        capitale_finale_affitti_nominale = results['valore_finale_nominale'] + results['totale_affitti_netti'] - results['commissione_iniziale'] - results['commissione_finale']
        capitale_finale_affitti_reale = results['valore_finale_reale'] + results['totale_affitti_netti_reale'] - results['commissione_iniziale'] - results['commissione_finale']
        st.write(f"{get_text('final_capital_rents_nominal')}{format_currency(capitale_finale_affitti_nominale)}**")
        st.write(f"{get_text('final_capital_rents_real')}{format_currency(capitale_finale_affitti_reale)}**")
        if results['commissione_iniziale'] > 0 or results['commissione_finale'] > 0:
            commissioni_totali = results['commissione_iniziale'] + results['commissione_finale']
            st.write(f"{get_text('total_commissions_deducted')}{format_currency(commissioni_totali)})*")
    with summary_col2:
        st.info(get_text('calculation_note'))

def render_real_estate_section():
    st.subheader(get_text('real_estate_analysis'))
    st.info(get_text('real_estate_info'))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**{get_text('base_params')}**")
        valore_immobile = st.number_input(
            get_text('property_value'), min_value=5000.00, value=200000.00, step=5000.00, key="real_estate_value")
        
        # NUOVI PARAMETRI: Costi reali sostenuti
        st.write(f"**💰 Costi Reali Sostenuti**")
        costo_acquisto = st.number_input(
            "Costo di Acquisto (€)", min_value=0.00, value=0.00, step=1000.00, key="real_estate_purchase_cost",
            help="Quanto hai effettivamente pagato per acquistare l'immobile. Se 0, usa il valore immobile per i calcoli.")
        costo_ristrutturazione = st.number_input(
            "Costo di Ristrutturazione (€)", min_value=0.00, value=0.00, step=1000.00, key="real_estate_renovation_cost",
            help="Costi sostenuti per ristrutturazioni, lavori, migliorie. Se 0, non viene considerato.")
        
        # Mostra l'analisi dei costi se inseriti
        if costo_acquisto > 0 or costo_ristrutturazione > 0:
            costo_totale_sostenuto = costo_acquisto + costo_ristrutturazione
            differenza = valore_immobile - costo_totale_sostenuto
            st.info(f"💰 Totale investito: {format_currency(costo_totale_sostenuto)}")
            if differenza > 0:
                st.success(f"✅ Plusvalore iniziale: +{format_currency(differenza)}")
            elif differenza < 0:
                st.error(f"⚠️ Minusvalore iniziale: {format_currency(differenza)}")
            else:
                st.info("⚖️ Investimento in pari")
        
        # MODIFICA PRINCIPALE: Input affitto mensile invece che annuale
        affitto_mensile = st.number_input(
            get_text('monthly_rent'), min_value=0.00, value=1000.00, step=50.00, key="real_estate_monthly_rent")
        
        # Calcola l'affitto annuo per i calcoli interni
        affitto_lordo = affitto_mensile * 12
        
        # Mostra l'affitto annuo calcolato
        if affitto_mensile > 0:
            st.info(f"{get_text('annual_rent_calculated')}{format_currency(affitto_lordo)}")
        
        rivalutazione_annua = st.number_input(
            get_text('annual_appreciation'), min_value=0.0, max_value=50.0, value=2.0, step=0.1, key="real_estate_appreciation")
        anni_investimento = st.number_input(
            get_text('investment_years'), min_value=1, value=10, step=1, key="real_estate_years")
        
        st.write(f"**{get_text('one_time_commissions')}**")
        commissione_iniziale = st.number_input(
            get_text('initial_commission'), min_value=0.00, value=0.00, step=100.00, key="real_estate_initial_commission",
            help=get_text('initial_commission_help'))
        commissione_finale = st.number_input(
            get_text('final_commission'), min_value=0.00, value=0.00, step=100.00, key="real_estate_final_commission",
            help=get_text('final_commission_help'))
    
    with col2:
        st.write(f"**{get_text('costs_expenses')}**")
        costi_assicurazione_euro = st.number_input(
            get_text('insurance_costs'), min_value=0.00, max_value=10000.00, value=250.00, step=50.00,
            key="real_estate_insurance_euro", help=get_text('insurance_help'))
        costi_gestione_euro = st.number_input(
            get_text('annual_fixed_costs'), min_value=0.00, max_value=100000.00, value=250.00, step=50.00,
            key="real_estate_annual_costs_euro", help=get_text('annual_costs_help'))
        manutenzione_straordinaria_perc = st.number_input(
            get_text('extraordinary_maintenance'), min_value=0.0, max_value=99.0, value=1.0, step=0.1, key="real_estate_maintenance")
        tassazione_affitti_perc = st.number_input(
            get_text('rent_taxation'), min_value=0.0, max_value=99.0, value=21.0, step=1.0, key="real_estate_tax_rate")
        tassa_catastale_perc = st.number_input(
            get_text('property_tax'), min_value=0.0, max_value=99.0, value=0.8, step=0.1,
            key="real_estate_cadastral_tax", help=get_text('property_tax_help'))
        st.write(f"**{get_text('mortgage_section')}**")
        rata_mutuo_mensile = st.number_input(
            get_text('monthly_mortgage'), min_value=0.00, max_value=10000.00, value=0.00, step=50.00, key="real_estate_mortgage_payment")
        anni_restanti_mutuo = st.number_input(
            get_text('remaining_mortgage_years'), min_value=0, max_value=50, value=0, step=1, key="real_estate_mortgage_years")
    
    with col3:
        st.write(f"**{get_text('economic_params')}**")
        periodo_sfitto_perc = st.number_input(
            get_text('vacancy_period'), min_value=0.0, max_value=100.0, value=5.0, step=1.0, key="real_estate_vacancy")
        inflazione_perc = st.number_input(
            get_text('annual_inflation'), min_value=0.0, max_value=100.0, value=2.0, step=0.1, key="real_estate_inflation")
        
        # Opzioni tradotte per il selectbox
        adjustment_options = [get_text('property_value_adj'), get_text('inflation_adj'), get_text('no_adjustment')]
        tipo_adeguamento = st.selectbox(
            get_text('rent_adjustment_mode'), adjustment_options, index=0,
            key="real_estate_adjustment_type", help=get_text('rent_adjustment_help'))
        adeguamento_affitto_anni = st.number_input(
            get_text('rent_adjustment_years'), min_value=1, max_value=99, value=4, step=1,
            key="real_estate_rent_adjustment_years", help=get_text('rent_adjustment_years_help'))

        if rata_mutuo_mensile > 0:
            rata_annua_mutuo = rata_mutuo_mensile * 12
            st.info(f"{get_text('annual_mortgage_rate')}{format_currency(rata_annua_mutuo)}")
            if anni_restanti_mutuo > 0:
                costo_totale_mutuo = rata_annua_mutuo * min(anni_restanti_mutuo, anni_investimento)
                st.info(f"{get_text('total_mortgage_cost')}{format_currency(costo_totale_mutuo)}")
        if tipo_adeguamento == get_text('property_value_adj'):
            st.info(get_text('property_value_adj_info'))
        elif tipo_adeguamento == get_text('inflation_adj'):
            st.info(get_text('inflation_adj_info'))
        else:
            st.warning(get_text('no_adj_info'))

    st.write(f"**{get_text('adjustment_notes')}**")
    note_col1, note_col2 = st.columns(2)
    with note_col1:
        st.write(get_text('monthly_rent_note'))
        st.write(get_text('property_value_note'))
        st.write(get_text('inflation_note'))
        st.write(get_text('no_adjustment_note'))
        st.write(get_text('management_costs_note'))
        st.write(get_text('insurance_costs_note'))
    with note_col2:
        st.write(get_text('monthly_calculation_note'))
        st.write(get_text('percentage_costs_note'))
        st.write(get_text('maintenance_taxes_note'))
        st.write(get_text('fixed_costs_note'))
        st.write(get_text('mortgage_note'))
        st.write(get_text('fixed_mortgage_note'))

    if st.button(get_text('calculate_button'), key="calc_real_estate"):
        try:
            # Converti le opzioni tradotte nei valori originali per i calcoli
            tipo_adeguamento_orig = tipo_adeguamento
            if tipo_adeguamento == get_text('property_value_adj'):
                tipo_adeguamento_orig = "Valore Immobile"
            elif tipo_adeguamento == get_text('inflation_adj'):
                tipo_adeguamento_orig = "Inflazione"
            elif tipo_adeguamento == get_text('no_adjustment'):
                tipo_adeguamento_orig = "Nessun Adeguamento"
            
            params = {
                'valore_immobile': valore_immobile,
                'costo_acquisto': costo_acquisto,
                'costo_ristrutturazione': costo_ristrutturazione,
                'affitto_lordo': affitto_lordo,  # Usa l'affitto annuale calcolato
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
                'tipo_adeguamento': tipo_adeguamento_orig,
                'commissione_iniziale': commissione_iniziale,
                'commissione_finale': commissione_finale
            }
            results = calculate_real_estate_investment_improved(params)
            display_real_estate_results_simplified(results, params)
        except Exception as e:
            st.error(f"{get_text('calculation_error')}{str(e)}")
            st.error(get_text('check_values'))
            st.exception(e)
