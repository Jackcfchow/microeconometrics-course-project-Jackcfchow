import numpy as np
import pandas as pd
from statsmodels.formula.api import wls
import statsmodels.api as sm

def get_table2_result(df_data, dep, result_dataframe ):
    df_data[dep].replace('  ', np.nan, inplace=True)
    data = df_data.dropna(subset=[dep])
    result = result_dataframe
    print(dep)
    fit = wls(dep + " ~  tr9 +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=True)
    result.loc[result["Dependent variable St"] == dep, "Parameter"] = fit.params["tr9"].round(3)
    result.loc[result["Dependent variable St"] == dep, "SE"] = fit.bse["tr9"].round(3)
    result.loc[result["Dependent variable St"] == dep, "P Value"] = fit.pvalues["tr9"]
    return(fit)



def get_ols_tsls_result(df_data, dep, result_dataframe ):
    #remember to setup a dataframe to write result
    #result = result.set_index('Dependent variable')

    df_data[dep].replace('  ', np.nan, inplace=True)
    data = df_data.dropna(subset=[dep])
    result = result_dataframe
    print(dep)

    # get the ols result
    ols = wls(dep + " ~  eng +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
# 2SLS: first stage esti: use idvar as IV of eng; and second stage
    fit_st1 = wls( "eng ~ idvar + C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    data['eng_hat'] = fit_st1.predict(data)
    fit_st2 = wls(dep + " ~  eng_hat +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    # fit_st2.summary()
    result.loc[result["Dependent variable St"] == dep, "OLS Parameter"] = ols.params["eng"].round(3)
    result.loc[result["Dependent variable St"] == dep, "OLS SE"] = ols.bse["eng"].round(3)
    result.loc[result["Dependent variable St"] == dep, "OLS P Value"] = ols.pvalues["eng"]
    result.loc[result["Dependent variable St"] == dep, "2SLS Parameter"] = fit_st2.params["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS SE"] = fit_st2.bse["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS P Value"] = fit_st2.pvalues["eng_hat"]
    return(ols,fit_st2)


def get_asterisk(data,P_value_col_name, Reg_name):
    Text = Reg_name +" Sig. level"
    data.loc[data[P_value_col_name] < 1, Text] = " "
    data.loc[data[P_value_col_name] <= 0.1, Text] = "*"
    data.loc[data[P_value_col_name] <= 0.05, Text] = "**"
    data.loc[data[P_value_col_name] <= 0.01, Text] = "***"



def get_asteris_and_coef(data,P_value_col_name, Reg_name, New_col_name):
    sig_level_name = Reg_name +" Sig. level"
    parameter_name = Reg_name +" Parameter"
    se_name = Reg_name +" SE"
    data.loc[data[P_value_col_name] < 1, sig_level_name] = " "
    data.loc[data[P_value_col_name] <= 0.1, sig_level_name] = "*"
    data.loc[data[P_value_col_name] <= 0.05, sig_level_name] = "**"
    data.loc[data[P_value_col_name] <= 0.01, sig_level_name] = "***"
    data[New_col_name] = (data[parameter_name].astype(str) + data[sig_level_name])
    #data.loc = data.loc.drop(columns=[parameter_level_name, "OLS P Value", "Coef Sig. level"])


def get_variable_full_name(data_full):
    # combine the result
    dictionary = dict([
        ("eng1", "Speaks English not well or better"),
        ("eng2", "Speaks English well or better"),
        ("eng3", "Speaks English very well"),
        ("eng", "English-speaking ability ordinal measure"),
        ("marriedpresent", "Is currently married with spouse present"),
        ("divorced", "Is currently divorced"),
        ("evermarried", "Has ever married"),
        ("spouseeng", "Spouse English-speaking ability ordinal measure"),
        ("marriednative", "Spouse is US-born"),
        ("couplesamebpld", "Spouse has the same country of birth"),
        ("couplesameancestry1", "Spouse has the same ancestry"),
        ("spouseage", "Spouse age"),
        ("spouseyrssch", "Spouse years of schooling"),
        ("spouselnwage", "Spouse log(wages last year)"),
        ("spouseworkedly", "Spouse worked last year"),
        ("bothworked", "Both worked last year"),
        ("nchild", "Number of children living in same household"),
        ("haskid", "Has a child living in same household"),
        ("nchild_spouse", "Number of children living in same household, only individuals married spouse present"),
        ("haskid_spouse", "Has a child living in same household, only individuals married with spouse present"),
        ("singleparent", "Is a single parent"),
        ("nevermarried_haskid", "Is a never married, single parent"),
        ("share_bpld_minusself", "Fraction of PUMA population from same country of birth"),
        ("abovemean_bpld2", "Fraction from same country of birth is above national mean for the country of birth"),
        ("ancestpct_minusself", "Fraction of PUMA population with same primary ancestry"),
        ("abovemean_ancestry2", "Fraction with same ancestry is above national mean for the primary ancestry")
    ])
    Dict_for_sumlist2 = dict([
        ("English-speaking ability ordinal measure", "Panel A. Regressors"),
        ("Age", "Panel A. Regressors"),
        ("Female", "Panel A. Regressors"),
        ("White", "Panel A. Regressors"),
        ("Black", "Panel A. Regressors"),
        ("Other", "Panel A. Regressors"),
        ("Asian/Pacific Islander", "Panel A. Regressors"),
        ("Multi", "Panel A. Regressors"),
        ("Hispdum", "Panel A. Regressors"),
        ("Years of schooling", "Panel A. Regressors"),
        ("Is currently married with spouse present", "Panel B. Marriage outcomes"),
        ("Is currently divorced", "Panel B. Marriage outcomes"),
        ("Has ever married", "Panel B. Marriage outcomes"),
        ("Spouse English-speaking ability ordinal measure", "Panel B. Marriage outcomes"),
        ("Spouse is US-born", "Panel B. Marriage outcomes"),
        ("Spouse has the same country of birth", "Panel B. Marriage outcomes"),
        ("Spouse has the same ancestry", "Panel B. Marriage outcomes"),
        ("Spouse age", "Panel B. Marriage outcomes"),
        ("Spouse years of schooling", "Panel B. Marriage outcomes"),
        ("Spouse log(wages last year)", "Panel B. Marriage outcomes"),
        ("Spouse worked last year", "Panel B. Marriage outcomes"),
        ("Both worked last year", "Panel B. Marriage outcomes"),
        ("Number of children living in same household", "Panel C. Fertility outcomes"),
        ("Has a child living in same household", "Panel C. Fertility outcomes"),
        ("Number of children living in same household, only individuals married spouse present",
         "Panel C. Fertility outcomes"),
        ("Has a child living in same household, only individuals married with spouse present",
         "Panel C. Fertility outcomes"),
        ("Is a single parent", "Panel C. Fertility outcomes"),
        ("Is a never married, single parent", "Panel C. Fertility outcomes"),
        ("Fraction of PUMA population from same country of birth", "Panel D. Residential location outcomes"),
        ("Fraction from same country of birth is above national mean for the country of birth",
         "Panel D. Residential location outcomes"),
        ("Fraction of PUMA population with same primary ancestry", "Panel D. Residential location outcomes"),
        ("Fraction with same ancestry is above national mean for the primary ancestry",
         "Panel D. Residential location outcomes")
    ])

    for i in data_full["Dependent variable St"]:
        data_full.loc[data_full["Dependent variable St"] == i, "Dependent variable"] = dictionary[i]
        data_full.loc[data_full["Dependent variable St"] == i, "Panel"] = Dict_for_sumlist2[i]

    data_full = data_full.set_index('Dependent variable')
    data_full = data_full.drop(columns=['Dependent variable St'])

    return (data_full)

def get_tsls_result_table4(df_data, dep , result_dataframe ,extra_contorl=""):
    #remember to setup a dataframe to write result
    #result = result.set_index('Dependent variable')

    df_data[dep].replace('  ', np.nan, inplace=True)
    data = df_data.dropna(subset=[dep])
    result = result_dataframe
    print(dep)
    if extra_contorl =="":
        fit_st1 = wls( "eng ~ idvar + C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum" +extra_contorl, data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
        data['eng_hat'] = fit_st1.predict(data)
        fit_st2 = wls(dep + " ~  eng_hat +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum" + extra_contorl, data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    else:
        fit_st1 = wls( "eng ~ idvar + C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum" +"+"+ extra_contorl, data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
        data['eng_hat'] = fit_st1.predict(data)
        fit_st2 = wls(dep + " ~  eng_hat +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum" +"+" + extra_contorl, data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    result.loc[result["Dependent variable St"] == dep, "2SLS Parameter"] = fit_st2.params["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS SE"] = fit_st2.bse["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS P Value"] = fit_st2.pvalues["eng_hat"]
    return(fit_st2)




def get_Durbin_Wu_Hausman_result(df, dep,result_frame):
    #setup a dataframe to write result
    #result = result.set_index('Dependent variable')

    df[dep].replace('  ', np.nan, inplace=True)
    data = df.dropna(subset=[dep])
    result_DWH= result_frame

    print(dep)

    fit_st1 = wls( "eng ~ idvar + C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    data['Epsilon']  = fit_st1.resid
    data['eng_hat'] = fit_st1.predict(data)
    test_reg = wls(dep + " ~  eng + Epsilon +C(agearr) + C(age) + C(bpld) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    result_DWH.loc[result_DWH["Dependent variable St"] == dep, "Epsilon Parameter"] = test_reg.params["Epsilon"].round(3)
    result_DWH.loc[result_DWH["Dependent variable St"] == dep, "Epsilon SE"] = test_reg.bse["Epsilon"].round(3)
    result_DWH.loc[result_DWH["Dependent variable St"] == dep, "Epsilon P Value"] = test_reg.pvalues["Epsilon"]


def get_ols_tsls_result_Robust2(df_data, dep, result_dataframe ):
    #remember to setup a dataframe to write result
    #result = result.set_index('Dependent variable')

    df_data[dep].replace('  ', np.nan, inplace=True)
    data = df_data.dropna(subset=[dep])
    result = result_dataframe
    print(dep)

# 2SLS: first stage esti: use idvar as IV of eng; and second stage
    fit_st1 = wls( "eng ~ idvar + C(agearr) + C(age) + C(bpld)+ C(statefip) + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    data['eng_hat'] = fit_st1.predict(data)
    fit_st2 = wls(dep + " ~  eng_hat +C(agearr) + C(age) + C(bpld)+ C(statefip)  + female + black + asianpi + other + multi + hispdum", data=data, weights=data["perwt2"] ).fit(cov_type='cluster', cov_kwds={'groups': data['bpld']}, use_t=False)
    # fit_st2.summary()
    result.loc[result["Dependent variable St"] == dep, "2SLS Parameter"] = fit_st2.params["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS SE"] = fit_st2.bse["eng_hat"].round(3)
    result.loc[result["Dependent variable St"] == dep, "2SLS P Value"] = fit_st2.pvalues["eng_hat"]
    result.loc[result["Dependent variable St"] == dep, "Adj R sq"] = fit_st2.rsquared_adj
    return(fit_st2)





def get_variable_full_name_table2(data_full):
    # combine the result
    dictionary = dict([
        ("eng1", "Speaks English not well or better"),
        ("eng2", "Speaks English well or better"),
        ("eng3", "Speaks English very well"),
        ("eng", "English-speaking ability ordinal measure"),
        ("marriedpresent", "Is currently married with spouse present"),
        ("divorced", "Is currently divorced"),
        ("evermarried", "Has ever married"),
        ("spouseeng", "Spouse English-speaking ability ordinal measure"),
        ("marriednative", "Spouse is US-born"),
        ("couplesamebpld", "Spouse has the same country of birth"),
        ("couplesameancestry1", "Spouse has the same ancestry"),
        ("spouseage", "Spouse age"),
        ("spouseyrssch", "Spouse years of schooling"),
        ("spouselnwage", "Spouse log(wages last year)"),
        ("spouseworkedly", "Spouse worked last year"),
        ("bothworked", "Both worked last year"),
        ("nchild", "Number of children living in same household"),
        ("haskid", "Has a child living in same household"),
        ("nchild_spouse", "Number of children living in same household, only individuals married spouse present"),
        ("haskid_spouse", "Has a child living in same household, only individuals married with spouse present"),
        ("singleparent", "Is a single parent"),
        ("nevermarried_haskid", "Is a never married, single parent"),
        ("share_bpld_minusself", "Fraction of PUMA population from same country of birth"),
        ("abovemean_bpld2", "Fraction from same country of birth is above national mean for the country of birth"),
        ("ancestpct_minusself", "Fraction of PUMA population with same primary ancestry"),
        ("abovemean_ancestry2", "Fraction with same ancestry is above national mean for the primary ancestry")
    ])
    dictionary2 = dict([
        ("Speaks English not well or better", "Panel A. English proficiency measures"),
        ("Speaks English well or better", "Panel A. English proficiency measures"),
        ("Speaks English very well", "Panel A. English proficiency measures"),
        ("English-speaking ability ordinal measure", "Panel A. English proficiency measures"),
        # ("Age", "Panel A. English proficiency measures"),
        # ("Female", "Panel A. Regressors"),
        # ("White", "Panel A. Regressors"),
        # ("Black", "Panel A. Regressors"),
        # ("Other", "Panel A. Regressors"),
        # ("Asian/Pacific Islander", "Panel A. Regressors"),
        # ("Multi", "Panel A. Regressors"),
        # ("Hispdum", "Panel A. Regressors"),
        # ("Years of schooling", "Panel A. Regressors"),
        ("Is currently married with spouse present", "Panel B. Marital status"),
        ("Is currently divorced", "Panel B. Marriage status"),
        ("Has ever married", "Panel B. Marriage status"),
        ("Spouse English-speaking ability ordinal measure", "Panel C. Spouse’s nativity and ethnicity"),
        ("Spouse is US-born", "Panel C. Spouse’s nativity and ethnicity"),
        ("Spouse has the same country of birth", "Panel C. Spouse’s nativity and ethnicity"),
        ("Spouse has the same ancestry", "Panel C. Spouse’s nativity and ethnicity"),
        ("Spouse age", "Panel D. Spouse’s age and education"),
        ("Spouse years of schooling", "Panel D. Spouse’s age and education"),
        ("Spouse log(wages last year)", "Panel E. Spouse’s labor market outcomes"),
        ("Spouse worked last year", "Panel E. Spouse’s labor market outcomes"),
        ("Both worked last year", "Panel E. Spouse’s labor market outcomes"),
        ("Number of children living in same household", "Panel F. Fertility"),
        ("Has a child living in same household", "Panel F. Fertility"),
        ("Number of children living in same household, only individuals married spouse present",
         "Panel F. Fertility"),
        ("Has a child living in same household, only individuals married with spouse present",
         "Panel F. Fertility"),
        ("Is a single parent", "Panel F. Fertility"),
        ("Is a never married, single parent", "Panel F. Fertility"),
        ("Fraction of PUMA population from same country of birth", "Panel G. Residential location"),
        ("Fraction from same country of birth is above national mean for the country of birth",
         "Panel G. Residential location"),
        ("Fraction of PUMA population with same primary ancestry", "Panel G. Residential location"),
        ("Fraction with same ancestry is above national mean for the primary ancestry",
         "Panel G. Residential location")
    ])

    for i in data_full["Dependent variable St"]:
        data_full.loc[data_full["Dependent variable St"] == i, "Dependent variable"] = dictionary[i]
    for j in data_full["Dependent variable"]:
        data_full.loc[data_full["Dependent variable"] == j, "Panel"] = dictionary2[j]
    data_full = data_full.drop(columns=['Dependent variable St'])
    data_full = data_full.set_index(['Panel',"Dependent variable"],inplace=False)
    return (data_full)

def get_variable_full_name_table3(data_full):
    dictionary = dict([
        ("eng1", "Speaks English not well or better"),
        ("eng2", "Speaks English well or better"),
        ("eng3", "Speaks English very well"),
        ("eng", "English-speaking ability ordinal measure"),
        ("marriedpresent", "Is currently married with spouse present"),
        ("divorced", "Is currently divorced"),
        ("evermarried", "Has ever married"),
        ("spouseeng", "Spouse English-speaking ability ordinal measure"),
        ("marriednative", "Spouse is US-born"),
        ("couplesamebpld", "Spouse has the same country of birth"),
        ("couplesameancestry1", "Spouse has the same ancestry"),
        ("spouseage", "Spouse age"),
        ("spouseyrssch", "Spouse years of schooling"),
        ("spouselnwage", "Spouse log(wages last year)"),
        ("spouseworkedly", "Spouse worked last year"),
        ("bothworked", "Both worked last year"),
        ("nchild", "Number of children living in same household"),
        ("haskid", "Has a child living in same household"),
        ("nchild_spouse", "Number of children living in same household, only individuals married spouse present"),
        ("haskid_spouse", "Has a child living in same household, only individuals married with spouse present"),
        ("singleparent", "Is a single parent"),
        ("nevermarried_haskid", "Is a never married, single parent"),
        ("share_bpld_minusself", "Fraction of PUMA population from same country of birth"),
        ("abovemean_bpld2", "Fraction from same country of birth is above national mean for the country of birth"),
        ("ancestpct_minusself", "Fraction of PUMA population with same primary ancestry"),
        ("abovemean_ancestry2", "Fraction with same ancestry is above national mean for the primary ancestry")
    ])
    dictionary2 = dict([
        ("Is currently married with spouse present", "Panel A. Marital status"),
        ("Is currently divorced", "Panel A. Marital status"),
        ("Has ever married", "Panel A. Marital status"),
        ("Spouse English-speaking ability ordinal measure", "Panel B. Spouse’s nativity and ethnicity"),
        ("Spouse is US-born", "Panel B. Spouse’s nativity and ethnicity"),
        ("Spouse has the same country of birth", "Panel B. Spouse’s nativity and ethnicity"),
        ("Spouse has the same ancestry", "Panel B. Spouse’s nativity and ethnicity"),
        ("Spouse age", "Panel C. Spouse’s age and education"),
        ("Spouse years of schooling", "Panel C. Spouse’s age and education"),
        ("Spouse log(wages last year)", "Panel D. Spouse’s labor market outcomes"),
        ("Spouse worked last year", "Panel D. Spouse’s labor market outcomes"),
        ("Both worked last year", "Panel D. Spouse’s labor market outcomes"),
        ("Number of children living in same household", "Panel E. Fertility"),
        ("Has a child living in same household", "Panel E. Fertility"),
        ("Number of children living in same household, only individuals married spouse present",
         "Panel E. Fertility"),
        ("Has a child living in same household, only individuals married with spouse present",
         "Panel E. Fertility"),
        ("Is a single parent", "Panel E. Fertility"),
        ("Is a never married, single parent", "Panel E. Fertility"),
        ("Fraction of PUMA population from same country of birth", "Panel F. Neighborhood outcomes"),
        ("Fraction from same country of birth is above national mean for the country of birth", "Panel F. Neighborhood outcomes"),
        ("Fraction of PUMA population with same primary ancestry", "Panel F. Neighborhood outcomes"),
        ("Fraction with same ancestry is above national mean for the primary ancestry", "Panel F. Neighborhood outcomes")

    ])

    for i in data_full["Dependent variable St"]:
        data_full.loc[data_full["Dependent variable St"] == i, "Dependent variable"] = dictionary[i]
    for j in data_full["Dependent variable"]:
        data_full.loc[data_full["Dependent variable"] == j, "Panel"] = dictionary2[j]
    data_full = data_full.set_index(['Panel',"Dependent variable"],inplace=False)
    data_full = data_full.drop(columns=['Dependent variable St'])

    return (data_full)

