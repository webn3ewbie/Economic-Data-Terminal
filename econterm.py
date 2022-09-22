import pandas as pd
import streamlit as st
import os
from fredapi import Fred

KEY = '9cbe93cd8132301fd46ad5e755944df0'
fred = Fred(api_key=KEY)


        
econ_dictionary = {
    # GDP
    'GDPC1': ['Real GDP $B'], 'A939RC0Q052SBEA': ['GDP/Capita'],
    'PCECC96':['TOTAL $B'],'DGDSRX1Q020SBEA':['Goods $B'],'PCESVC96':['Services $B'],
    'GPDIC1': ['TOTAL $B'], 'PNFIC1': ['Nonresidential $B'], 'PRFIC1': ['Residential $B'], 'CBIC1': ['Change in Private Inventory'],
    'GCEC1': ['TOTAL $B'], 'FGCEC1': ['Federal $B'], 'SLCEC1': ['State/Local $B'],
    'NETEXC': ['NET Exports $B'], 'EXPGSC1': ['Exports $B'], 'IMPGSC1': ['Imports $B'],
    ##Housing Market
    'NHSUSSPT': ['Total New Houses Sold (1,000s of Units)'],'EXHOSLUSM495S': ['Existing Houses Sold (1,000s of Units)'], 'MNMFS': ['Months on Maarket'], 'USSTHPI': ['House Price Index'],
    # Manufacturing Market
    'IPMAN': ['Industrial Production Manufacturing Index'], 'IPG331S': ['Durable Goods - Primary Metals'],
    'IPG334S': ['Durable Goods - Computer and Electronic Products'], 'IPG3361T3S': ['Durable Goods - Motor Vehicles and Parts'],
    'IPG337S': ['Durable Goods - Furniture and related products'], 'IPG315A6S': ['Non-Durable Goods - Apparel and Leather Goods'],
    'GFDEBTN': ['Public Debt $M'], 'GFDEGDQ188S': ['Public Debt/Gross GDP Ratio'], 'MTSDS133FMS': ['Federal Surplus or Deficit'], 'FYFSGDA188S': ['Federal Surplus or Deficit as Ratio of GDP'],
    'NFCI': ['NFCI'],

    #Volatility
    'VIXCLS': [' VIX'], 'GVZCLS': [' CBOE Gold ETF Volatility'], 'OVXCLS': ['CBOE Crude Oil ETF Volatility Index'],       
    #Recession Risks
    'T10Y3M': [' 10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity'], 'RECPROUSM156N':['Smoothed U.S. Recession Probabilities'], 'SAHMREALTIME':['Real-time Sahm Rule Recession Indicator'], 'JHGDPBRINDX':['GDP-Based Recession Indicator Index'],      
    #Commodities
    'DCOILWTICO':[' Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma'],'DHHNGSP':['Henry Hub Natural Gas Spot Price'], 'GASREGW':['US Regular All Formulations Gas Price'], 'APU0000708111':['Average Price: Eggs, Grade A, Large (Cost per Dozen) in U.S. City Average'],
    'APU0000FF1101':['Average Price: Chicken Breast, Boneless (Cost per Pound) in U.S. City Average'], 'APU0000703112':['Average Price: Ground Beef, 100% Beef (Cost per Pound) in U.S. City Average'], 'APU000072610':['Average Price: Electricity per Kilowatt-Hour in U.S. City Average'], 
    'PCOPPUSDM':['Global price of Copper"'], 'PALUMUSDM':['Global price of Aluminum'], 'PNICKUSDM':['Global price of Nickel'], 'APU0000701111':['Average Price: Flour, White, All Purpose (Cost per Pound) in U.S. City Average '],
    # Labor Market
    'UNRATE': ['U3 Rate %'], 'U6RATE': ['U6 Rate %'], 'NROU': ['Natural Unemployment Rate %'],
    'CIVPART': ['Cumm. LFPR %'], 'LNS11300002': ['Women LFPR%'], 'LNS11300001': ['Men LFPR%'],
    'LNS11300012': ["16-19yrs LFPR %"], 'LNS11300036': ['20-24yrs LFPR %'] ,'LNS11300060': ['25-54yrs LFPR %'], 'LNS11324230': ['55+yrs LFPR %'],
    'LNS11300003': ['White LFPR %'], 'LNS11300006': ['Black LFPR %'], 'LNS11300009': ['Hispanic LFPR %'], 'LNU01332183': ['Asian LFPR %'],
    'ICSA': ['Initial Jobless Claims'], 'IC4WSA': ['4 wk MA of Initial Claims'], 'CCSA': ['Continued Claims (Insured Unempl.)'], 'CC4WSA': ['4wk MA of Continued Claims'],
    'FRBKCLMCIM': ['Labor Market Momentum'], 'FRBKCLMCILA': ['Labor Market Level of Activity'],
    # Fed's Tools
    'DFF': ['Daily EFF rate'], 'FEDTARRM': ['EFF Midpoint Projection'],
    'T20YIEM':  ['20 yr CPI'], 'EFFR': ['Median EFFR'],
    'INTDSRUSM193N': ["Fed's Discount Rate"], 'IORR': ['% on Required Reserves'], 'IOER': ['% on Excess Reserves'],
    'RPONAGYD': ['Repos Purchased $B'], 'RRPONTSYD': ['Repos Sold $B'],
    'DGS30': ['30 Year %'], 'DGS20': ['20 Year %'],'DGS10': ['10 Year %'], 'DGS5': ['5 Year %'] ,'DGS2': ['2 Year %'],
    'RESPPLLDTXAWXCH52NWW': ['Weekly Net Change in General Account $M'],
    #Inflation
    'USACPIALLMINMEI': ['Inflation level'], 'PPIACO': ['PPI Level'], 'PCEC96': ['Real PCE Level'],
    'DSPIC96': ['Real Disposable Income $B']
        
    }


# Helper Functions
def to_df(series_name, start, end):
    series = fred.get_series(series_name, start, end)
    df = pd.DataFrame(series, columns=econ_dictionary[series_name])
    # df.index = df.index.date
    return df

def show_chart(df):
    if len(df) > 1:
        st.line_chart(df)
    else:
        st.warning('\Select an earlier START date to view a line chart over time')

major_selection = st.sidebar.selectbox(
    'Explore Data for:',
    ('Home','Overall Economic Activity', 'Labor Market',
     "Fed's Tools", "Inflation","Volatility","Commodities", "Recession Risks")
)
if major_selection == 'Home':
        st.write("# Welcome to MACRO Terminal ")
        st.markdown(
            """ 
            MACRO Terminal is an open-source Streamlit app built specifically to analyze equities, bonds, commodities, currencies, and cryptos. MACRO Terminal leverages the FRED API, which allow users to analyze a wide ranging number of macro datasets.
            
           
            MACRO Terminal consists of multiple unique dashboards that feature Overall Economic Activity, Labor Markets, Fed Tools, Inflation, Volatility, Commodities, and Recession Risks. 
            Select a dashboard and see what MACRO Terminal can do! 
            
            
            #### Want to learn more?
            - Check out the repo [Here](https://github.com/webn3ewbie/Economic-Data-Terminal)
            - Connect with me on [LinkedIn](https://www.linkedin.com/in/joseph-biancamano/)
            - Ask a question in the Streamlit community [forums](https://discuss.streamlit.io)
            
            
            Please note this app is NOT financial advice,  nor are any dashboards intended to help guide financial decisions!
        """
        )
if major_selection == 'Overall Economic Activity':
    st.title('Overall Economic Activity')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date
    st.info("An Indicator's chart may not be available because \n"
            "data has not been released for the specified time frame.")
    st.subheader('Gross Domestic Product (GDP)')
    gdp = to_df('GDPC1', start_date, end_date)
    show_chart(gdp)
    st.write('Updates *Quarterly*')

    st.subheader('GDP/Capita')
    gdp_percap = to_df('A939RC0Q052SBEA', start_date, end_date)
    show_chart(gdp_percap)
    st.write('Updates *Quarterly*')

    st.subheader('Use the dropdown menu to look at the GDP through its 4 main components')
    gdp_components = st.selectbox("4 Main Components",
                                  ('Consumption', 'Investment', 'Government Expenditure', 'Net Exports'))
    if gdp_components == 'Consumption':
        st.subheader('Personal Consumption Expenditures')
        c = to_df('PCECC96', start_date, end_date)
        c_goods = to_df('DGDSRX1Q020SBEA', start_date, end_date)
        c_services = to_df('PCESVC96', start_date, end_date)
        c_total = pd.concat([c, c_goods, c_services], axis=1)

        show_chart(c_total)
        st.write('Updates *Quarterly*')

    if gdp_components == 'Investment':
        st.subheader('Gross Private Domestic Investment')
        st.write("Where the majority of Investments are *Nonresidential*")

        i = to_df('GPDIC1', start_date, end_date)
        i_res = to_df('PRFIC1', start_date, end_date)
        i_nonres = to_df('PNFIC1', start_date, end_date)
        i_inventory = to_df('CBIC1', start_date, end_date)
        i_total = pd.concat([i, i_res, i_nonres], axis=1)

        show_chart(i_total)
        st.write('Updates *Quarterly*')

        inv_change = st.checkbox('Change in Real Private Inventory')
        if inv_change:
            st.line_chart(i_inventory)
            st.write('Updates *Quarterly*')

    if gdp_components == 'Government Expenditure':
        st.subheader('Government Consumption Expenditures and Investment')
        gov_exandinv = to_df('GCEC1', start_date, end_date)
        gov_fed = to_df('FGCEC1', start_date, end_date)
        gov_statelocal = to_df('SLCEC1', start_date, end_date)
        gov_total = pd.concat([gov_exandinv, gov_fed, gov_statelocal], axis=1)

        show_chart(gov_total)
        st.write('Updates *Quarterly*')

    if gdp_components == 'Net Exports':
        st.subheader('Net Exports of Goods and Services')
        nex = to_df('NETEXC', start_date, end_date)
        exports = to_df('EXPGSC1', start_date, end_date)
        imports = to_df('IMPGSC1', start_date, end_date)
        netexports = pd.concat([nex, exports, imports], axis=1)

        show_chart(netexports)
        st.write('Updates *Quarterly*')

    st.header('Housing Market')
    st.subheader('New Home Sales')
    new_homes = to_df('NHSUSSPT', start_date, end_date)
    show_chart(new_homes)
    st.write('Updates *Monthly*')

    st.subheader('Existing Home Sales')
    exist_homes = to_df('EXHOSLUSM495S', start_date, end_date)
    show_chart(exist_homes)
    st.write('Updates *Monthly*')

    st.subheader('Median Months on Market for New Homes')
    months_on_market = to_df('MNMFS', start_date, end_date)
    show_chart(months_on_market)
    st.write('Updates *Monthly*')

    st.subheader('Federal Housing Financing Agency Price Index')
    fhfi = to_df('USSTHPI', start_date, end_date)
    show_chart(fhfi)
    st.write('Updates *Quarterly*')

    st.header('Manufacturing Sector')
    naics_ipmanu = to_df('IPMAN', start_date, end_date)
    show_chart(naics_ipmanu)
    st.write('Updates *Monthly*')

    metals = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Primary Metal (NAICS=331)')
    compelec_prods = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Computer and Electronic Products (NAICS=334)')
    vehicles = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Motor Vehicles and Parts (NAICS=3361-3)')
    furniture = st.checkbox('Industrial Production: Manufacturing - Durable Goods - Furniture and Related Goods (NAICS=337)')
    apparel = st.checkbox('Industrial Production: Manufacturing - Non Durable Goods - Apparel and Leather Goods (NAICS=315,6)')

    metals_df = to_df('IPG331S', start_date, end_date)
    compelec_prods_df = to_df('IPG334S', start_date, end_date)
    vehicles_df = to_df('IPG3361T3S', start_date, end_date)
    furniture_df = to_df('IPG337S', start_date, end_date)
    apparel_df = to_df('IPG315A6S', start_date, end_date)


    manu_checks = [metals, compelec_prods, vehicles, furniture, apparel]
    manudf_list = [metals_df, compelec_prods_df, vehicles_df, furniture_df, apparel_df]
    manu_sectors_todisp = []

    #checks checkboxes
    for int in range(len(manu_checks)):
        if manu_checks[int]:
            manu_sectors_todisp.append(manudf_list[int])
    if len(manu_sectors_todisp) == 0:
        st.warning('No Boxes are checked')

    if len(manu_sectors_todisp) > 0:
        final_manudf = pd.concat(manu_sectors_todisp, axis=1)
        show_chart(final_manudf)
        st.write('Updates *Monthly*')

    st.header('US National Balance Sheet')
    st.subheader('Federal Debt: Total Public Debt')
    debt = to_df('GFDEBTN', start_date, end_date)
    show_chart(debt)
    st.write('Updates *Quarterly*')

    st.subheader('Debt/GDP Ratio')
    debt_to_gdp = to_df('GFDEGDQ188S', start_date, end_date)
    show_chart(debt_to_gdp)
    st.write('Updates *Quarterly*')

    st.subheader('Federal Surplus or Deficit')
    surp_or_def = to_df('MTSDS133FMS', start_date, end_date)
    show_chart(surp_or_def)
    st.write('Updates *Monthly*')

    st.subheader('Surplus or Deficit/GDP Ratio')
    surp_or_def_ratio = to_df('FYFSGDA188S', start_date, end_date)
    show_chart(surp_or_def_ratio)
    st.write('Updates *Monthly*')

    st.header('Credit Market')
    st.subheader('National Financial Conditions Index ')
    nfci = to_df('NFCI', start_date, end_date)
    show_chart(nfci)
    st.write('Updates *Weekly*')
    
if major_selection == 'Labor Market':
    st.title('Labor Market')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date
    

    st.subheader('Unemployment Rates (U3 and U6)')
    u3_rate = to_df('UNRATE',start_date, end_date)
    u6_rate = to_df('U6RATE', start_date, end_date)
    unemployment_rates = pd.concat([u3_rate, u6_rate], axis=1)
    show_chart(unemployment_rates)
    st.write('Updates Monthly')

    st.subheader('Natural Rate of Unemploymnet (Long-Term)')
    natural_urate = to_df('NROU', start_date, end_date)
    show_chart(natural_urate)
    st.write('Updates Quarterly')


    st.subheader('Labor Force Participation Rates (LFPR)')
    lfpr_total = to_df('CIVPART', start_date, end_date)
    show_chart(lfpr_total)
    st.write('Updates Quarterly')

    lfpr_select = st.selectbox('View the LFPR by demographic:',
                               ('Age', 'Gender', 'Race'))

    if lfpr_select == 'Age':
        lfpr_younger = to_df('LNS11300012', start_date, end_date)
        lfpr_young = to_df('LNS11300036', start_date, end_date)
        lfpr_middle = to_df('LNS11300060', start_date, end_date)
        lfpr_old = to_df('LNS11324230', start_date, end_date)
        lfpr_age_df = pd.concat([lfpr_younger, lfpr_young,
                                 lfpr_middle, lfpr_old], axis=1)
        show_chart(lfpr_age_df)

    if lfpr_select == 'Gender':
        lfpr_female = to_df('LNS11300002', start_date, end_date)
        lfpr_male = to_df('LNS11300001', start_date, end_date)
        lfpr_gender_df = pd.concat([lfpr_female, lfpr_male], axis=1)
        show_chart(lfpr_gender_df)

    if lfpr_select == 'Race':
        white_lfpr = st.checkbox('White')
        black_lfpr = st.checkbox('Black')
        hispanic_lpr = st.checkbox('Hispanic')
        asian_lfpr = st.checkbox('Asian')

        white_lfpr_df = to_df('LNS11300003', start_date, end_date)
        black_lfpr_df = to_df('LNS11300006', start_date, end_date)
        hispanic_lpr_df = to_df('LNS11300009', start_date, end_date)
        asian_lfpr_df = to_df('LNU01332183', start_date, end_date)

        lfpr_checks = [white_lfpr, black_lfpr, hispanic_lpr, asian_lfpr]
        lfpr_df_list = [white_lfpr_df, black_lfpr_df, hispanic_lpr_df, asian_lfpr_df]
        lfpr_races_todisp = []

        col1, col2 = st.beta_columns([2,2])

        # checks checkboxes
        for int in range(len(lfpr_df_list)):
            if lfpr_checks[int]:
                lfpr_races_todisp.append(lfpr_df_list[int])
        if len(lfpr_races_todisp) == 0:
            st.warning('No Boxes are checked')

        if len(lfpr_races_todisp) > 0:
            final_lfpr_races = pd.concat(lfpr_races_todisp, axis=1)
            with col1:
                # st.header of Combinations of races
                #Cut the |T00:... from the Datetime Index
                show_chart(final_lfpr_races)
                st.write('Updates *Monthly*')
            with col2:
                st.write(final_lfpr_races)

    st.subheader('Initial Jobless Claims')
    init_claims = to_df('ICSA', start_date, end_date)
    init_ma_claims = to_df('IC4WSA', start_date, end_date)
    init_total = pd.concat([init_claims, init_ma_claims], axis=1)
    show_chart(init_total)
    st.write('Updates Weekly')

    st.subheader('Continuing Jobless Claims')
    cont_claims = to_df('CCSA', start_date, end_date)
    cont_ma_claims = to_df('CC4WSA', start_date, end_date)
    cont_total = pd.concat([cont_claims, cont_ma_claims], axis=1)
    show_chart(cont_total)
    st.write('Updates Weekly')

    st.subheader('KC Fed Labor Market Conditions: Momentum and Overall Activity')
    kc_momentum = to_df('FRBKCLMCIM', start_date, end_date)
    kc_activity = to_df('FRBKCLMCILA', start_date, end_date)
    kc = pd.concat([kc_momentum, kc_activity], axis=1)
    show_chart(kc)
    st.write('Updates Monthly')

if major_selection == "Fed's Tools":
    st.title('Fed Tools')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date
    st.subheader("Fed's Funds Rate")
    eff = to_df('DFF', start_date, end_date)
    show_chart(eff)
    st.write('Updates Daily')

    st.subheader("FOMC FFR Midpoint Project")
    effproj = to_df('FEDTARRM', start_date, end_date)
    show_chart(effproj)
    st.write('Updates Yearly')

    #st.subheader("LIBOR Rates")

    st.subheader('EFFR (Lending Rates between Banks)')
    effr = to_df('EFFR', start_date, end_date)
    show_chart(effr)
    st.write('Updates Daily')

    st.subheader('Discount Rate')
    discount = to_df('INTDSRUSM193N', start_date, end_date)
    show_chart(discount)
    st.write('Updates Monthly')

    st.subheader('IR on Required Reserves')
    ir_rr = to_df('IORR', start_date, end_date)
    show_chart(ir_rr)
    st.write('Updates Daily')

    st.subheader('IR on Excess Reserves')
    ir_er = to_df('IOER', start_date, end_date)
    show_chart(ir_er)
    st.write('Updates Daily')

    st.header('Open Market Operations: Purchase and sell Repos')
    buy_repos = to_df('RPONAGYD', start_date, end_date)
    sell_repos = to_df('RRPONTSYD', start_date, end_date)
    repos = pd.concat([buy_repos, sell_repos], axis = 1)
    show_chart(repos)
    st.write('Updates Daily')
    st.write(repos)

    st.header("Yield Curves") 
    st.subheader('Treasury Yields')
    yield_30 = to_df('DGS30', start_date, end_date)
    yield_20 = to_df('DGS20', start_date, end_date)
    yield_10 = to_df('DGS10', start_date, end_date)
    yield_5 = to_df('DGS5', start_date, end_date)
    yield_2 = to_df('DGS2', start_date, end_date)
    yields = pd.concat([yield_30, yield_10, yield_20 ,yield_5 , yield_2], axis=1)
    show_chart(yields)

    st.header("Fed's Balance Sheet and Holdings")
    st.subheader('Fed Balance Sheet: Weekly Net Change in General Account')
    ga_weekly = to_df('RESPPLLDTXAWXCH52NWW', start_date, end_date)
    show_chart(ga_weekly)
     
if major_selection == 'Inflation':
    st.title('Inflation')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date

    st.subheader("Inflation Target from CPI")
    infl_20 = to_df('T20YIEM', start_date, end_date)
    show_chart(infl_20)
    st.write('Updates Monthly')

    st.subheader('CPI based on ALL US Products')
    cpi = to_df('USACPIALLMINMEI', start_date, end_date)
    show_chart(cpi)
    st.write('Updates Monthly')

    st.subheader('PPI based on ALL US Commodities')
    ppi = to_df('PPIACO', start_date, end_date)
    show_chart(ppi)
    st.write('Updates Monthly')

    st.subheader('Real PCE')
    pce = to_df('PCEC96', start_date, end_date)
    show_chart(pce)
    st.write('Updates Monthly')

    st.subheader('Real Disposable Income')
    r_di = to_df('DSPIC96', start_date, end_date)
    show_chart(r_di)
    
if major_selection == 'Volatility':
    st.title('Volatility')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date

    st.subheader("CBOE Volatility Index")
    vix = to_df('VIXCLS', start_date, end_date)
    show_chart(vix)
    
    st.subheader(" CBOE Gold ETF Volatility Index")
    gvix = to_df('GVZCLS', start_date, end_date)
    show_chart(gvix)
    
    st.subheader(" CBOE Crude Oil ETF Volatility Index")
    cvix = to_df('OVXCLS', start_date, end_date)
    show_chart(cvix)
    
    vixs = pd.concat([vix, gvix,cvix],axis=1)
    show_chart(vixs)
        
if major_selection == 'Commodities':
    st.title('Commodities')
    st.subheader("Select Commodity Type")
    com_components = st.selectbox("3 Main Components",
                                  ('Energy', 'Metals', 'Agriculture'))
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date
    
    if com_components == 'Energy':
        wti = to_df('DCOILWTICO', start_date, end_date)
        ng = to_df('DHHNGSP', start_date, end_date)
        gasa = to_df('GASREGW', start_date, end_date)
        elc = to_df('APU000072610', start_date, end_date)
        etotal = pd.concat([wti, ng, gasa, elc], axis=1)
        st.subheader("Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma")
        show_chart(wti)
        st.subheader("Henry Hub Natural Gas Spot Price")
        show_chart(ng)
        st.subheader("US Regular All Formulations Gas Price")
        show_chart(gasa, y= 'US Dollars')
        st.subheader("Average Price: Electricity per Kilowatt-Hour in U.S. City Average")
        show_chart(elc)
      
    
    if com_components == 'Agriculture':
        egg = to_df('APU0000708111', start_date, end_date)
        chk = to_df('APU0000FF1101', start_date, end_date)
        bef = to_df('APU0000703112', start_date, end_date)
        flo = to_df('APU0000701111', start_date, end_date)
        etotal = pd.concat([egg, chk, bef], axis=1)
        st.subheader("Average Price: Eggs, Grade A, Large (Cost per Dozen) in U.S. City Average")
        show_chart(egg)
        st.subheader("Average Price: Chicken Breast, Boneless (Cost per Pound) in U.S. City Average")
        show_chart(chk)
        st.subheader("Average Price: Ground Beef, 100% Beef (Cost per Pound) in U.S. City Average")
        show_chart(bef)
        st.subheader('Average Price: Flour, White, All Purpose (Cost per Pound) in U.S. City Average ')
        show_chart(flo)
        
    if com_components == 'Metals':
         cop = to_df('PCOPPUSDM', start_date, end_date)
         alu = to_df('PALUMUSDM', start_date, end_date)
         nkl = to_df('PNICKUSDM', start_date, end_date)
         etotal = pd.concat([cop, alu, nkl], axis=1)
         
         st.subheader("Global price of Copper")
         show_chart(cop)
         st.subheader("Global price of Aluminum")
         show_chart(alu)
         st.subheader("Global price of Nickel")
         show_chart(nkl)
 
if major_selection == 'Recession Risks':
    st.title('Recession Risks')
    start_date = st.date_input('START Date')
    end_date = st.date_input('END Date')
    date_condition = start_date < end_date
    
    st.subheader("10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity")
    ttm = to_df('T10Y3M', start_date, end_date)
    show_chart(ttm)
        
    st.subheader("Smoothed U.S. Recession Probabilities")
    srp = to_df('RECPROUSM156N', start_date, end_date)
    show_chart(srp)
    
    st.subheader("Real-time Sahm Rule Recession Indicator")
    srr = to_df('SAHMREALTIME', start_date, end_date)
    show_chart(srr)

    st.subheader("GDP-Based Recession Indicator Index")
    gdpr = to_df('JHGDPBRINDX', start_date, end_date)
    show_chart(gdpr)
