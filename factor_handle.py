# -*- coding:utf-8 -*-

import statsmodels.api as sm
import os
import pandas as pd
from ConstValue import (BARRA_PATH,
                        FACTOR_LIST,
                        FORMAT
                        )

def neutralize(factor, tradeDate, field=FACTOR_LIST):

    """
    返回被中性化之后的因子值

    Params:
    ==========
    factor: pd.Series，需要被中性化的因子
    tradeDate: str or datetime， 当前交易日
    filed: 所需字段,可以是列表
    """

    factor_copy = factor.copy()
    tradeDate = pd.core.tools.datetimes.to_datetime(tradeDate).strftime(FORMAT)
    barra_factor = pd.read_hdf(os.path.join(BARRA_PATH, '.'.join(tradeDate, 'h5')), 'table')[field]

    model = sm.OLS(factor_copy.loc[barra_factor.index], barra_factor).fit()

    return model.resid


def fill_(factor, tradeDate, field=FACTOR_LIST):

    """
    填补缺失值
    Params:
    ==========
    factor: pd.Series，需要被填补的因子
    tradeDate: str or datetime， 当前交易日
    filed: 所需字段,可以是列表
    """

    factor_copy = factor.copy()
    tradeDate = pd.core.tools.datetimes.to_datetime(tradeDate).strftime(FORMAT)
    barra_factor = pd.read_hdf(os.path.join(BARRA_PATH, '.'.join(tradeDate, 'h5')), 'table')[field]
    factor_copy = factor_copy.loc[barra_factor.index]
    factor_NNA = factor_copy.dropna()

    model = sm.OLS(factor_NNA, barra_factor.loc[factor_NNA.index]).fit()
    factor_copy = factor_copy.fillna(model.predict(barra_factor))

    return factor_copy