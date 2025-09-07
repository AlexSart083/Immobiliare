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
- **ROI**: {get_text('roi_note')}
- **ROE**: {get_text('roe_note')}
{get_text('property_tax_note')}
""")
    st.markdown("---")
    st.markdown(f"*{get_text('developed_by')}*")

def display_real_estate_results_simplified(results, params):
    st.success(f"**{get_text('results_title')}**")

    res_col1, res_col2, res_col3 = st.columns(3)

    # ... tutto il codice esistente per le prime 3 colonne ...

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
            
def render_real_estate_section():
    st.subheader(get_text('real_estate_analysis'))
    st.info(get_text('real_estate_info'))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**{get_text('base_params')}**")
        valore_immobile = st.number_input(
            get_text('property_value'), min_value=5000.00, value=200000.00, step=5000.00, key="real_estate_value")
        affitto_mensile = st.number_input(
            get_text('monthly_rent'), min_value=0.00, value=1000.00, step=50.00, key="real_estate_monthly_rent")
        # Calcola l'affitto annuo per i calcoli interni
        if affitto_mensile > 0:
            st.info(f"{get_text('annual_rent_calculated')}{format_currency(affitto_lordo)}")
        affitto_lordo = affitto_mensile * 12        
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
