import streamlit as st

# Dizionari delle traduzioni
TRANSLATIONS = {
    'it': {
        # Header
        'page_title': 'Calcolatore Investimenti Immobiliari',
        'app_title': '🏠 Calcolatore Investimenti Immobiliari',
        'app_subtitle': '💡 Analisi Completa con Rivalutazione, Inflazione e Adeguamento Affitti',
        
        # Language selector
        'language': 'Lingua',
        'select_language': 'Seleziona Lingua',
        
        # Real Estate Section
        'real_estate_analysis': '🏘️ Analisi Investimento Immobiliare',
        'real_estate_info': '💡 Stima con rivalutazione, inflazione, mutuo e adeguamento affitti personalizzabile',
        
        # Base Parameters
        'monthly_rent': 'Affitto Lordo Mensile (€)',
        'annual_rent_calculated': '💰 Affitto Annuo Calcolato: ',
        'rent_calculation_notes': 'ℹ️ Note sul Calcolo Affitto:',
        'monthly_rent_note': '• **Affitto Mensile**: Inserito dall\'utente, moltiplicato x12 per i calcoli',
        'monthly_rent_input': 'Affitto mensile inserito',
        'calculated_annually': 'Calcolato annualmente per l\'analisi',        
        'base_params': '🏠 Parametri Base Immobile',
        'property_value': 'Valore Immobile (€)',
        'annual_rent': 'Affitto Lordo Annuo (€)',
        'annual_appreciation': 'Rivalutazione Annua (%)',
        'investment_years': 'Anni di Investimento',
        'one_time_commissions': 'Commissioni una tantum',
        'initial_commission': 'Commissione Iniziale (€)',
        'initial_commission_help': 'Costi di acquisto una tantum (es. agenzia, notaio)',
        'final_commission': 'Commissione Finale (€)',
        'final_commission_help': 'Costi di vendita una tantum (es. agenzia)',
        
        # Costs and Expenses
        'costs_expenses': '💸 Costi e Spese',
        'insurance_costs': 'Costi Assicurazione Annui (€)',
        'insurance_help': 'Costi fissi annui per assicurazione. Verranno adeguati all\'inflazione.',
        'annual_fixed_costs': 'Costi Fissi Annui (€)',
        'annual_costs_help': 'Costi fissi annui (es. amministratore, pulizie, piccole manutenzioni). Verranno adeguati all\'inflazione.',
        'extraordinary_maintenance': 'Manutenzione Straordinaria Annua (%)',
        'rent_taxation': 'Tassazione su Affitti (%)',
        'property_tax': 'Tassa di proprietà (% valore immobile)',
        'property_tax_help': '⚠️ Valore semplificato - Il calcolo della tassa di proprietà in questa applicazione è basato sul **valore dell\'immobile**. È importante sapere che per il calcolo ufficiale dell\'imposta in Italia è legata alla **rendita catastale** e al **coefficiente catastale** dell\'immobile.',
        'mortgage_section': '🏦 Mutuo (se presente)',
        'monthly_mortgage': 'Rata Mutuo Mensile (€)',
        'remaining_mortgage_years': 'Anni Restanti Mutuo',
        
        # Economic Parameters
        'economic_params': '📊 Parametri Economici e Adeguamenti',
        'vacancy_period': 'Periodo Annuo Sfitto (%)',
        'annual_inflation': 'Inflazione Annua (%)',
        'rent_adjustment_mode': 'Modalità Adeguamento Affitto',
        'rent_adjustment_help': 'Scegli come adeguare l\'affitto nel tempo',
        'rent_adjustment_years': 'Adeguamento Affitto ogni (Anni)',
        'rent_adjustment_years_help': 'Ogni quanti anni l\'affitto viene adeguato secondo la modalità scelta',
        
        # Adjustment modes
        'property_value_adj': 'Valore Immobile',
        'inflation_adj': 'Inflazione',
        'no_adjustment': 'Nessun Adeguamento',
        
        # Info messages
        'annual_mortgage_rate': '💰 Rata Annua Mutuo: ',
        'total_mortgage_cost': '💸 Costo Totale Mutuo nel Periodo: ',
        'property_value_adj_info': '🏠 Affitto adeguato al valore rivalutato dell\'immobile',
        'inflation_adj_info': '📈 Affitto adeguato al tasso di inflazione',
        'no_adj_info': '⚡ Affitto rimane fisso per tutto il periodo',
        
        # Notes
        'adjustment_notes': 'ℹ️ Note sui Metodi di Adeguamento e Costi:',
        'property_value_note': '• **Valore Immobile**: L\'affitto mantiene la stessa % del valore immobile',
        'inflation_note': '• **Inflazione**: L\'affitto cresce con l\'inflazione',
        'no_adjustment_note': '• **Nessun Adeguamento**: Affitto fisso (perdita potere d\'acquisto)',
        'management_costs_note': '• **Costi Gestione**: Importo fisso adeguato annualmente all\'inflazione',
        'insurance_costs_note': '• **Costi Assicurazione**: Importo fisso adeguato annualmente all\'inflazione',
        'percentage_costs_note': '• Costi percentuali si aggiornano sempre al valore dell\'immobile',
        'maintenance_taxes_note': '• Manutenzione e tasse calcolate su valore corrente',
        'fixed_costs_note': '• Assicurazione e gestione: costi fissi + inflazione',
        'mortgage_note': '• **Mutuo**: Se presente, viene considerato fino alla scadenza',
        'fixed_mortgage_note': '• Rate mutuo sono fisse e non si adeguano all\'inflazione',
        
        # Calculate button
        'calculate_button': '🏠 Calcola Investimento Immobiliare',
        
        # Results
        'results_title': '🎯 Risultati Analisi Investimento Immobiliare',
        'property_value_section': '🏠 Valore Immobile:',
        'initial_value': '• Valore Iniziale: ',
        'final_nominal_value': '• **Valore Finale (Nominale): ',
        'final_real_value': '• **Valore Finale (Reale): ',
        'capital_gain_nominal': '• Plusvalenza (Nominale): ',
        'total_appreciation': '• Rivalutazione Totale: ',
        
        'rent_analysis': '💰 Analisi Affitti:',
        'initial_rent': '• Affitto Iniziale: ',
        'final_rent': '• **Affitto Finale: ',
        'total_rent_growth': '• **Crescita Affitto Totale: ',
        'total_net_rents_nominal': '• **Totale Affitti Netti (Nominale): ',
        'total_net_rents_real': '• **Totale Affitti Netti (Reale): ',
        'average_monthly_real': '• **Media Affitti Mensili Reale: ',
        'adjustment_mode': '• Modalità Adeguamento: **',
        
        'total_return': '📈 Rendimento Totale:',
        'total_return_nominal': '• **Rendimento Totale (Nominale): ',
        'total_return_real': '• **Rendimento Totale (Reale): ',
        'total_mortgage_costs': '• **Totale Costi Mutuo: ',
        'initial_commissions': '• **Commissioni Iniziali: ',
        'final_commissions': '• **Commissioni Finali: ',
        'return_perc_nominal': '• Rendimento % (Nominale): ',
        
        # Performance metrics
        'performance_metrics': '📊 Metriche di Performance:',
        'cagr_nominal_metric': '🏆 CAGR Nominale',
        'cagr_real_metric': '🏆 CAGR Reale',
        'main_metric_caption': '✅ Metrica principale per confronti',
        'inflation_considered_caption': '✅ Considerando inflazione',
        'why_cagr': '💡 Perché CAGR?',
        'cagr_explanation': 'Il CAGR normalizza i rendimenti su base annua e permette confronti diretti con altri investimenti',
        'roi_section': '📈 ROI (Return on Investment):',
        'roe_section': '🎯 ROE (Return on Equity):',
        'roi_nominal_total': '• ROI Totale Nominale: ',
        'roi_real_total': '• **ROI Totale Reale: ',
        'roi_annualized_real': '• ROI Annualizzato Reale: ',
        'initial_investment': '• Investimento Iniziale: ',
        'roe_nominal_total': '• ROE Totale Nominale: ',
        'roe_real_total': '• **ROE Totale Reale: ',
        'roe_annualized_real': '• ROE Annualizzato Reale: ',
        'roi_annualized_nominal': '• ROI Annualizzato Nominale: ',
        'roe_annualized_nominal': '• ROE Annualizzato Nominale: ',        
        
        'mortgage_analysis': '🏦 Analisi Mutuo:',
        'total_mortgage_costs_years': '• **Totale Costi Mutuo ',
        'years_suffix': ' anni: ',
        'annual_vs_initial_rent': '• Rata annua vs Affitto iniziale: ',
        'mortgage_free_years': '✅ Ultimi ',
        'years_without_payment': ' anni senza rata',
        'sustainable_mortgage': '✅ Mutuo sostenibile (< 50% affitto)',
        'challenging_mortgage': '⚠️ Mutuo impegnativo (50-70% affitto)',
        'risky_mortgage': '🚨 Mutuo rischioso (> 70% affitto)',
        'return_without_mortgage': '📊 Rendimento senza mutuo: +',
        
        'investment_summary': '📋 Riepilogo Investimento:',
        'final_capital_rents_nominal': '• **Capitale Finale + Affitti (Nominale): ',
        'final_capital_rents_real': '• **Capitale Finale + Affitti (Reale): ',
        'total_commissions_deducted': '• *(Già detratte commissioni totali: ',
        
        'calculation_note': '📝 Nota: Questo calcolo è basato su assunzioni semplificate. I mercati immobiliari reali sono influenzati da numerosi fattori non considerati (domanda/offerta locale, normative, condizioni economiche, ecc.). Consulta sempre un consulente finanziario prima di investire.',
        
        # Footer
        'disclaimer_title': '⚠️ **DISCLAIMER IMPORTANTE**',
        'legal_notice': '**🚨 AVVISO LEGALE - LEGGERE ATTENTAMENTE**',
        'educational_purpose': '📚 **Scopo Didattico**: Questa applicazione è stata sviluppata esclusivamente a scopo educativo e dimostrativo per illustrare concetti di investimento immobiliare.',
        'not_financial_advice': '🚫 **Non è Consulenza Finanziaria**: I calcoli e le informazioni fornite NON costituiscono consigli di investimento, raccomandazioni immobiliari o consulenza professionale.',
        'data_accuracy': '⚠️ **Accuratezza dei Dati**: I valori calcolati potrebbero essere imprecisi o non riflettere la complessità del mercato immobiliare reale.',
        'responsibility': '📊 **Responsabilità**: Lo sviluppatore declina ogni responsabilità per decisioni di investimento basate sui risultati ottenuti.',
        'recommendation': '💡 **Raccomandazione**: Consultare SEMPRE un consulente immobiliare e finanziario qualificato prima di investire.',
        'privacy': '🔒 **Privacy**: I dati inseriti non vengono salvati o trasmessi.',
        
        'technical_notes': '📝 Note Tecniche:',
        'appreciation_note': '- **Rivalutazione**: Apprezzamento annuo del valore dell\'immobile',
        'rent_adjustment_note': '- **Adeguamento Affitto**: Modalità di aggiornamento del canone nel tempo',
        'nominal_values_note': '- **Valori Nominali**: Senza considerare l\'inflazione',
        'real_values_note': '- **Valori Reali**: Considerando l\'effetto dell\'inflazione sul potere d\'acquisto',
        'cagr_note': 'Tasso di crescita annuale composto (metrica principale per confronti)',
        'roi_note': 'Return on Investment - rendimento totale sull\'investimento iniziale',
        'roe_note': 'Return on Equity - rendimento sul capitale proprio (importante con leverage)',
        'property_tax_note': '- **Tassa di Proprietà**: Calcolo semplificato basato sul valore dell\'immobile (nella realtà dipende dalla rendita catastale)',

        'tir_nominal': 'TIR Nominale',
        'tir_real': 'TIR Reale',
        'tir_note': 'Tasso Interno di Rendimento - considera il timing dei flussi di cassa',
        'tir_calculation_na': 'Calcolo TIR non possibile',
        'tir_deflated': 'TIR deflazionato',
        'internal_rate_return': 'Tasso interno rendimento',
        'main_metrics': 'Metriche Principali',
        'secondary_metrics': 'Metriche Secondarie',
        'metrics_comparison': 'Confronto Metriche',
        'nominal_values': 'Valori Nominali',
        'real_values': 'Valori Reali',
        'cagr_explanation': 'Tasso di crescita annuale composto - normalizza i rendimenti e permette confronti diretti',
        'tir_explanation': 'Tasso Interno di Rendimento - considera il timing dei flussi di cassa ed è lo standard nel settore immobiliare',
        'metrics_info': 'Entrambe sono ottime per confrontare con altri investimenti',
        'cashflow_well_distributed': 'CAGR e TIR sono molto simili - flussi di cassa ben distribuiti nel tempo',
        'small_difference_normal': 'Piccola differenza tra CAGR e TIR - normale per investimenti immobiliari',
        'significant_difference_warning': 'Differenza significativa tra CAGR e TIR - analizzare la distribuzione dei flussi di cassa',
        'compound_annual_growth': 'Crescita annuale composta',
        'considering_inflation': 'Considerando inflazione',

        'initial_monthly_rent': '• Affitto Mensile Iniziale: ',
        'final_monthly_rent': '• **Affitto Mensile Finale: ',
        'monthly_payment_vs_initial_rent': '• Rata mensile vs Affitto mensile iniziale: ',
        'sustainable_mortgage_monthly': '✅ Mutuo sostenibile (< 50% affitto mensile)',
        'challenging_mortgage_monthly': '⚠️ Mutuo impegnativo (50-70% affitto mensile)',
        'risky_mortgage_monthly': '🚨 Mutuo rischioso (> 70% affitto mensile)',
        'monthly_rent_growth': '• Crescita Affitto Mensile: ',
        'rent_monthly_vs_annual': '• Mensile vs Annuale',

        'monthly_calculation_note': '• I calcoli interni usano il valore annuale (mensile × 12)',
        'mortgage_monthly_analysis': '• L\'analisi mutuo considera sia confronti mensili che annuali',

        
        'developed_by': '*Sviluppata da **AS** con la collaborazione di **KIM** 🐱 - Versione per fini didattici*',
        
        # Error messages
        'calculation_error': '❌ Errore nel calcolo immobiliare: ',
        'check_values': 'Verifica che tutti i valori siano corretti.',
    },
    
    'en': {
        # Header
        'page_title': 'Real Estate Investment Calculator',
        'app_title': '🏠 Real Estate Investment Calculator',
        'app_subtitle': '💡 Complete Analysis with Appreciation, Inflation and Rent Adjustments',
        
        # Language selector
        'language': 'Language',
        'select_language': 'Select Language',
        
        # Real Estate Section
        'real_estate_analysis': '🏘️ Real Estate Investment Analysis',
        'real_estate_info': '💡 Estimate with appreciation, inflation, mortgage and customizable rent adjustments',
        
        # Base Parameters
        'monthly_rent': 'Monthly Gross Rent (€)',
        'annual_rent': 'Annual Gross Rent (€)',  # Mantieni per i calcoli
        'annual_rent_calculated': '💰 Calculated Annual Rent: ',
        'rent_calculation_notes': 'ℹ️ Rent Calculation Notes:',
        'monthly_rent_note': '• **Monthly Rent**: User input, multiplied x12 for calculations',
        'monthly_rent_input': 'Monthly rent input',
        'calculated_annually': 'Calculated annually for analysis',        
        'base_params': '🏠 Base Property Parameters',
        'property_value': 'Property Value (€)',
        'annual_appreciation': 'Annual Appreciation (%)',
        'investment_years': 'Investment Years',
        'one_time_commissions': 'One-time commissions',
        'initial_commission': 'Initial Commission (€)',
        'initial_commission_help': 'One-time purchase costs (e.g. agency, notary)',
        'final_commission': 'Final Commission (€)',
        'final_commission_help': 'One-time selling costs (e.g. agency)',
        
        # Costs and Expenses
        'costs_expenses': '💸 Costs and Expenses',
        'insurance_costs': 'Annual Insurance Costs (€)',
        'insurance_help': 'Fixed annual insurance costs. Will be adjusted for inflation.',
        'annual_fixed_costs': 'Annual Fixed Costs (€)',
        'annual_costs_help': 'Fixed annual costs (e.g. administrator, cleaning, small maintenance). Will be adjusted for inflation.',
        'extraordinary_maintenance': 'Annual Extraordinary Maintenance (%)',
        'rent_taxation': 'Rent Taxation (%)',
        'property_tax': 'Property tax (% property value)',
        'property_tax_help': '⚠️ Simplified value - Property tax calculation in this application is based on **property value**. It\'s important to know that for official tax calculation in Italy it\'s linked to the **cadastral income** and **cadastral coefficient** of the property.',
        'mortgage_section': '🏦 Mortgage (if present)',
        'monthly_mortgage': 'Monthly Mortgage Payment (€)',
        'remaining_mortgage_years': 'Remaining Mortgage Years',
        
        # Economic Parameters
        'economic_params': '📊 Economic Parameters and Adjustments',
        'vacancy_period': 'Annual Vacancy Period (%)',
        'annual_inflation': 'Annual Inflation (%)',
        'rent_adjustment_mode': 'Rent Adjustment Mode',
        'rent_adjustment_help': 'Choose how to adjust rent over time',
        'rent_adjustment_years': 'Rent Adjustment every (Years)',
        'rent_adjustment_years_help': 'How often rent is adjusted according to the chosen mode',
        
        # Adjustment modes
        'property_value_adj': 'Property Value',
        'inflation_adj': 'Inflation',
        'no_adjustment': 'No Adjustment',
        
        # Info messages
        'annual_mortgage_rate': '💰 Annual Mortgage Payment: ',
        'total_mortgage_cost': '💸 Total Mortgage Cost in Period: ',
        'property_value_adj_info': '🏠 Rent adjusted to revalued property value',
        'inflation_adj_info': '📈 Rent adjusted to inflation rate',
        'no_adj_info': '⚡ Rent remains fixed for the entire period',
        
        # Notes
        'adjustment_notes': 'ℹ️ Notes on Adjustment Methods and Costs:',
        'property_value_note': '• **Property Value**: Rent maintains the same % of property value',
        'inflation_note': '• **Inflation**: Rent grows with inflation',
        'no_adjustment_note': '• **No Adjustment**: Fixed rent (loss of purchasing power)',
        'management_costs_note': '• **Management Costs**: Fixed amount adjusted annually for inflation',
        'insurance_costs_note': '• **Insurance Costs**: Fixed amount adjusted annually for inflation',
        'percentage_costs_note': '• Percentage costs always update to property value',
        'maintenance_taxes_note': '• Maintenance and taxes calculated on current value',
        'fixed_costs_note': '• Insurance and management: fixed costs + inflation',
        'mortgage_note': '• **Mortgage**: If present, considered until maturity',
        'fixed_mortgage_note': '• Mortgage payments are fixed and don\'t adjust for inflation',
        
        # Calculate button
        'calculate_button': '🏠 Calculate Real Estate Investment',
        
        # Results
        'results_title': '🎯 Real Estate Investment Analysis Results',
        'property_value_section': '🏠 Property Value:',
        'initial_value': '• Initial Value: ',
        'final_nominal_value': '• **Final Value (Nominal): ',
        'final_real_value': '• **Final Value (Real): ',
        'capital_gain_nominal': '• Capital Gain (Nominal): ',
        'total_appreciation': '• Total Appreciation: ',
        
        'rent_analysis': '💰 Rent Analysis:',
        'initial_rent': '• Initial Rent: ',
        'final_rent': '• **Final Rent: ',
        'total_rent_growth': '• **Total Rent Growth: ',
        'total_net_rents_nominal': '• **Total Net Rents (Nominal): ',
        'total_net_rents_real': '• **Total Net Rents (Real): ',
        'average_monthly_real': '• **Average Monthly Real Rent: ',
        'adjustment_mode': '• Adjustment Mode: **',
        
        'total_return': '📈 Total Return:',
        'total_return_nominal': '• **Total Return (Nominal): ',
        'total_return_real': '• **Total Return (Real): ',
        'total_mortgage_costs': '• **Total Mortgage Costs: ',
        'initial_commissions': '• **Initial Commissions: ',
        'final_commissions': '• **Final Commissions: ',
        'return_perc_nominal': '• Return % (Nominal): ',
        
        # Performance metrics
        'performance_metrics': '📊 Performance Metrics:',
        'cagr_nominal_metric': '🏆 Nominal CAGR',
        'cagr_real_metric': '🏆 Real CAGR',
        'main_metric_caption': '✅ Main metric for comparisons',
        'inflation_considered_caption': '✅ Considering inflation',
        'why_cagr': '💡 Why CAGR?',
        'cagr_explanation': 'CAGR normalizes returns on an annual basis and allows direct comparisons with other investments',
        'roi_section': '📈 ROI (Return on Investment):',
        'roe_section': '🎯 ROE (Return on Equity):',
        'roi_nominal_total': '• Total Nominal ROI: ',
        'roi_real_total': '• **Total Real ROI: ',
        'roi_annualized_real': '• Annualized Real ROI: ',
        'initial_investment': '• Initial Investment: ',
        'roe_nominal_total': '• Total Nominal ROE: ',
        'roe_real_total': '• **Total Real ROE: ',
        'roe_annualized_real': '• Annualized Real ROE: ',
        'roi_annualized_nominal': '• Annualized Nominal ROI: ',
        'roe_annualized_nominal': '• Annualized Nominal ROE: ',        
        
        'mortgage_analysis': '🏦 Mortgage Analysis:',
        'total_mortgage_costs_years': '• **Total Mortgage Costs ',
        'years_suffix': ' years: ',
        'annual_vs_initial_rent': '• Annual payment vs Initial rent: ',
        'mortgage_free_years': '✅ Last ',
        'years_without_payment': ' years without payments',
        'sustainable_mortgage': '✅ Sustainable mortgage (< 50% rent)',
        'challenging_mortgage': '⚠️ Challenging mortgage (50-70% rent)',
        'risky_mortgage': '🚨 Risky mortgage (> 70% rent)',
        'return_without_mortgage': '📊 Return without mortgage: +',
        
        'investment_summary': '📋 Investment Summary:',
        'final_capital_rents_nominal': '• **Final Capital + Rents (Nominal): ',
        'final_capital_rents_real': '• **Final Capital + Rents (Real): ',
        'total_commissions_deducted': '• *(Total commissions already deducted: ',
        
        'calculation_note': '📝 Note: This calculation is based on simplified assumptions. Real estate markets are influenced by numerous factors not considered (local supply/demand, regulations, economic conditions, etc.). Always consult a financial advisor before investing.',
        
        # Footer
        'disclaimer_title': '⚠️ **IMPORTANT DISCLAIMER**',
        'legal_notice': '**🚨 LEGAL NOTICE - READ CAREFULLY**',
        'educational_purpose': '📚 **Educational Purpose**: This application has been developed exclusively for educational and demonstrative purposes to illustrate real estate investment concepts.',
        'not_financial_advice': '🚫 **Not Financial Advice**: The calculations and information provided do NOT constitute investment advice, real estate recommendations or professional consulting.',
        'data_accuracy': '⚠️ **Data Accuracy**: Calculated values may be inaccurate or not reflect the complexity of real estate markets.',
        'responsibility': '📊 **Responsibility**: The developer disclaims all responsibility for investment decisions based on the results obtained.',
        'recommendation': '💡 **Recommendation**: ALWAYS consult a qualified real estate and financial advisor before investing.',
        'privacy': '🔒 **Privacy**: Entered data is not saved or transmitted.',
        
        'technical_notes': '📝 Technical Notes:',
        'appreciation_note': '- **Appreciation**: Annual appreciation of property value',
        'rent_adjustment_note': '- **Rent Adjustment**: Method of updating rent over time',
        'nominal_values_note': '- **Nominal Values**: Without considering inflation',
        'real_values_note': '- **Real Values**: Considering inflation\'s effect on purchasing power',
        'cagr_note': 'Compound Annual Growth Rate (main metric for comparisons)',
        'roi_note': 'Return on Investment - total return on initial investment',
        'roe_note': 'Return on Equity - return on own capital (important with leverage)',
        'property_tax_note': '- **Property Tax**: Simplified calculation based on property value (in reality depends on cadastral income)',

        'tir_nominal': 'Nominal IRR',
        'tir_real': 'Real IRR',
        'tir_note': 'Internal Rate of Return - considers cash flow timing',
        'tir_calculation_na': 'IRR calculation not possible',
        'tir_deflated': 'Deflated IRR',
        'internal_rate_return': 'Internal rate of return',
        'main_metrics': 'Main Metrics',
        'secondary_metrics': 'Secondary Metrics',
        'metrics_comparison': 'Metrics Comparison',
        'nominal_values': 'Nominal Values',
        'real_values': 'Real Values',
        'cagr_explanation': 'Compound Annual Growth Rate - normalizes returns and enables direct comparisons',
        'tir_explanation': 'Internal Rate of Return - considers cash flow timing and is the real estate industry standard',
        'metrics_info': 'Both are excellent for comparing with other investments',
        'cashflow_well_distributed': 'CAGR and IRR are very similar - well-distributed cash flows over time',
        'small_difference_normal': 'Small difference between CAGR and IRR - normal for real estate investments',
        'significant_difference_warning': 'Significant difference between CAGR and IRR - analyze cash flow distribution',
        'compound_annual_growth': 'Compound annual growth',
        'considering_inflation': 'Considering inflation',

        'initial_monthly_rent': '• Initial Monthly Rent: ',
        'final_monthly_rent': '• **Final Monthly Rent: ',
        'monthly_payment_vs_initial_rent': '• Monthly payment vs Initial monthly rent: ',
        'sustainable_mortgage_monthly': '✅ Sustainable mortgage (< 50% monthly rent)',
        'challenging_mortgage_monthly': '⚠️ Challenging mortgage (50-70% monthly rent)',
        'risky_mortgage_monthly': '🚨 Risky mortgage (> 70% monthly rent)',
        'monthly_rent_growth': '• Monthly Rent Growth: ',
        'rent_monthly_vs_annual': '• Monthly vs Annual',
        'monthly_calculation_note': '• Internal calculations use annual value (monthly × 12)',
        'mortgage_monthly_analysis': '• Mortgage analysis considers both monthly and annual comparisons',
        
        'developed_by': '*Developed by **AS** in collaboration with **KIM** 🐱 - Educational version*',
        
        # Error messages
        'calculation_error': '❌ Real estate calculation error: ',
        'check_values': 'Please check that all values are correct.',
    }
}

def get_text(key, default_lang='it'):
    """
    Ottiene il testo tradotto per la lingua corrente
    """
    # Ottieni la lingua dalla sessione, default italiano
    current_lang = st.session_state.get('language', default_lang)
    
    # Restituisce il testo nella lingua corrente o in italiano se non trovato
    return TRANSLATIONS.get(current_lang, TRANSLATIONS['it']).get(key, key)

def set_language(lang):
    """
    Imposta la lingua nella sessione
    """
    st.session_state.language = lang
    
def get_current_language():
    """
    Restituisce la lingua corrente
    """
    return st.session_state.get('language', 'it')

def render_language_selector():
    """
    Renderizza il selettore di lingua
    """
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        current_lang = get_current_language()
        lang_options = {'Italiano': 'it', 'English': 'en'}
        
        # Trova la chiave corrente per il selectbox
        current_key = 'Italiano' if current_lang == 'it' else 'English'
        
        selected_lang = st.selectbox(
            get_text('language'),
            options=list(lang_options.keys()),
            index=list(lang_options.keys()).index(current_key),
            key="language_selector"
        )
        
        # Aggiorna la lingua se è cambiata
        new_lang = lang_options[selected_lang]
        if new_lang != current_lang:
            set_language(new_lang)
            st.rerun()
