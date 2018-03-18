import tushare as ts
import pandas as pd


BARRA_PATH = 'E:/industry_citic/barra_factor'
RET_PATH = 'E:/industry_citic/returns/'
DAY_RISK_PATH = 'E:/industry_citic/riskmodel_d'
MONTH_RISK_PATH = 'E:/industry_citic/riskmodel_m'
FORMAT = '%Y%m%d'
FACTOR_LIST = [u'Beta', u'Momentum', u'Size', u'Earning Yield', u'Growth', u'Leverge', u'NLSIZE', u'Value', u'Liquidity', u'Volatility', u'交通运输', u'房地产', u'煤炭', u'家电', u'机械', u'国防军工', u'纺织服装',
               u'计算机', u'医药', u'电力及公用事业', u'银行', u'通信', u'食品饮料', u'基础化工', u'建材', u'建筑', u'汽车', u'电子元器件', u'农林牧渔', u'钢铁', u'餐饮旅游', u'有色金属', u'石油石化', u'传媒', u'商贸零售', u'非银行金融', u'轻工制造', u'综合', u'电力设备']

TRADING_CAL = map(lambda x: x.strftime('%Y%m%d'), pd.DatetimeIndex(
        ts.trade_cal().set_index('calendarDate').groupby('isOpen').get_group(1).index))

TRADING_CAL = pd.Series(TRADING_CAL, index=TRADING_CAL)
TRADING_CAL.index = pd.DatetimeIndex(TRADING_CAL.index)