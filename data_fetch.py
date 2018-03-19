# -*- coding:utf-8 -*-

from ConstValue import (BARRA_PATH,
                        RET_PATH,
                        FORMAT,
                        DAY_RISK_PATH,
                        MONTH_RISK_PATH,
                        FACTOR_LIST,
                        TRADING_CAL
                        )
import pandas as pd
import os


def RMExposureDayGet(secID, ticker, tradeDate, beginDate, endDate, field=FACTOR_LIST):

    """
    该表反映了个股对各风格因子和行业因子的暴露值。

    Params:
    ==============
    secID: 证券内部编码，一串流水号,可先通过DataAPI.SecIDGet获取到，可以是列表,secID、ticker、tradeDate至少选择一个
    ticker: 证券在证券市场通用的交易代码。,可以是列表,secID、ticker、tradeDate至少选择一个
    tradeDate: 交易日期，,secID、ticker、tradeDate至少选择一个
    beginDate: 交易日的起始日期，,可空
    endDate: 交易日的截止日期,可空
    field: 所需字段,可以是列表
    注意：要么出现tradeDate, 要么出现beginDate和endDate
    """
    if secID and ticker:
        raise ValueError(u"secID和ticker至多一个非空")

    secid = []

    if secID or ticker:

        if secID:
            secid = secID
        else:
            secid = map(lambda x: x + '.SH' if x[0] == '6' else x + '.SZ', ticker)

    if beginDate and endDate and tradeDate:

        raise ValueError(u"beginDate, endDate, tradeDate不能同时有值")

    

    if tradeDate:
        tradeDate = pd.core.tools.datetimes.to_datetime(tradeDate).strftime(FORMAT)
        barra_factor = pd.read_hdf(os.path.join(BARRA_PATH, '.'.join(tradeDate, 'h5')), 'table')[field]
        if secid:
            return barra_factor.loc[secid, :].dropna()
        return barra_factor

    elif beginDate and endDate:
        iterator = pd.DataFrame()

        for date in TRADING_CAL[beginDate : endDate]:
            barra_factor = pd.read_hdf(os.path.join(BARRA_PATH, '.'.join(date, 'h5')), 'table')[field]
            if secid:
                barra_factor = barra_factor.loc[secid,:].dropna()
            barra_factor['Date'] = date
            barra_factor['Code'] = barra_factor.index
            iterator = pd.concat([iterator, barra_factor])
        iterator.index = range(iterator.shape[0])
        result = pd.DataFrame()

        for factor in field:
            factor_value = iterator.pivot(index='Date', columns='Code', values=factor).stack()
            result[factor] = factor_value

    else:       
        raise ValueError(u"beginDate、endDate、tradeDate至少选择一个")

        return result



def RMFactorRetDayGet(beginDate, endDate, tradeDate, field=FACTOR_LIST):

    """
    返回风险因子在指定时间段内的日收益率
    
    Params:
    ===========
    beginDate: 交易日的起始日期,beginDate、endDate、tradeDate至少选择一个
    endDate: 交易日的截止日期，beginDate、endDate、tradeDate至少选择一个
    tradeDate: 交易日期，beginDate、endDate、tradeDate至少选择一个
    field: 所需字段,可以是列表
    注意：要么出现tradeDate, 要么出现beginDate和endDate
    returns: Series
    """

    factor_returns = pd.read_hdf(os.path.join(RET_PATH, '.'.join('factor_returns', 'h5')), 'table')

    if beginDate and endDate and tradeDate:

        raise ValueError(u"beginDate, endDate, tradeDate不能同时有值")

    if tradeDate:
        return factor_returns.loc[tradeDate].loc[field]

    elif beginDate and endDate:
        return factor_returns.loc[beginDate : endDate].loc[field]

    else:
        raise ValueError(u"beginDate、endDate、tradeDate至少选择一个")




def RMCovarineGet(beginDate, endDate, tradeDate, freq, field=FACTOR_LIST):

    """
    返回日风险矩阵
    Params:
    =========
    beginDate: 交易日的起始日期,beginDate、endDate、tradeDate至少选择一个
    endDate: 交易日的截止日期,beginDate、endDate、tradeDate至少选择一个
    tradeDate: 交易日期，beginDate、endDate、tradeDate至少选择一个
    field: 所需字段,可以是列表
    注意：要么出现tradeDate, 要么出现beginDate和endDate
    """
    if beginDate and endDate and tradeDate:
        raise ValueError(u"beginDate, endDate, tradeDate不能同时有值")

    RISK_PATH = ''
    if freq == 'M':
        RISK_PATH = MONTH_RISK_PATH
    if freq == 'D':
        RISK_PATH == DAY_RISK_PATH

    if tradeDate:

        tradeDate = pd.core.tools.datetimes.to_datetime(tradeDate).strftime(FORMAT)
        return pd.read_hdf(os.path.join(DAY_RISK_PATH, '.'.join(tradeDate, 'h5')), 'common_risk').loc[field, field]

    if beginDate and endDate:
        result = dict()

        for date in TRADING_CAL[beginDate : endDate]:

            covarince_matrix = pd.read_hdf(os.path.join(DAY_RISK_PATH, '.'.join(date, 'h5')), 'common_risk').loc[field, field]
            result[date] = covarince_matrix
        return pd.Panel(result)

    else:
        raise ValueError(u"beginDate、endDate、tradeDate至少选择一个")

def RMSpecificRiskGet(secID, ticker, beginDate, endDate, tradeDate, freq, field=FACTOR_LIST):

    """
    返回给定频率下的股票特异风险

    Params:
    =============
    secID: 证券内部编码，一串流水号,可先通过DataAPI.SecIDGet获取到，可以是列表,secID、ticker、tradeDate至少选择一个
    ticker: 证券在证券市场通用的交易代码。,可以是列表,secID、ticker、tradeDate至少选择一个
    tradeDate: 交易日期，,secID、ticker、tradeDate至少选择一个
    beginDate: 交易日的起始日期，,可空
    endDate: 交易日的截止日期,可空
    注意：要么出现tradeDate, 要么出现beginDate和endDate
    """


    if beginDate and endDate and tradeDate:
        raise ValueError(u"beginDate, endDate, tradeDate不能同时有值")

    if secID and ticker:
        raise ValueError(u"secID和ticker至多一个非空")

    secid = []

    if secID or ticker:

        if secID:
            secid = secID
        else:
            secid = map(lambda x: x + '.SH' if x[0] == '6' else x + '.SZ', ticker)


    RISK_PATH = ''

    if freq == 'M':
        RISK_PATH = MONTH_RISK_PATH
    if freq == 'D':
        RISK_PATH == DAY_RISK_PATH

    if tradeDate:
        sprisk =  pd.read_hdf(os.path.join(RISK_PATH, '.'.join(tradeDate, 'h5')), 'specific_risk')
        if secid:
            sprisk = sprisk.loc[secid,:].dropna()
        return sprisk


    elif beginDate and endDate:
        SP_RISK = pd.DataFrame()

        for date in TRADING_CAL[beginDate : endDate]:

            sprisk = pd.read_hdf(os.path.join(RISK_PATH, '.'.join(date, 'h5')), 'specific_risk').to_frame('sprisk')
            if secid:
                sprisk = sprisk.loc[secid,:].dropna()
            sprisk['Date'] = date
            sprisk['Code'] = sprisk.index
            SP_RISK = pd.concat([SP_RISK, sprisk])

        SP_RISK = SP_RISK.pivot(index='Date', columns='Code', values='sprisk').stack()
        return SP_RISK

    else:
        raise ValueError(u"beginDate、endDate、tradeDate至少选择一个")











