"""
Author: Hugo
Date: 2024-08-19 15:10:04
LastEditors: shen.lan123@gmail.com
LastEditTime: 2024-08-21 09:34:15
Description: 
"""

"""
Author: Hugo
Date: 2024-08-19 15:10:04
LastEditors: shen.lan123@gmail.com
LastEditTime: 2024-08-19 15:10:28
Description: 
"""

import pandas as pd
import backtrader as bt
import empyrical as ep
import pyfolio as pf
from typing import Union

__all__ = [
    "get_strategy_return",
    "get_strategy_cumulative_return",
    "trans_minute_to_daily",
    "check_index_tz"
]


def get_strategy_return(
    strat: bt.Cerebro,
) -> pd.Series:
    """
    获取策略的收益率数据。

    参数：
        - strat: bt.Cerebro 对象，策略对象。


    返回：
        - pd.Series 对象，策略的收益率数据。
    """
    return pd.Series(strat.analyzers.getbyname("time_return").get_analysis())


def trans_minute_to_daily(minutes_close: pd.Series) -> pd.Series:
    """
    将分钟级别的收盘价转换为日级别的收盘价。

    参数：
        minutes_close (pd.Series): 分钟级别的收盘价数据。

    返回：
        pd.Series: 日级别的收盘价数据。
    """

    return minutes_close.resample("D").last().dropna()


def get_strategy_cumulative_return(
    strat: bt.Cerebro,
    starting_value: int = 0,
) -> pd.Series:
    """
    获取策略的累计收益率数据。

    参数：
        - strat: bt.Cerebro 对象，策略对象。


    返回：
        - pd.Series 对象，策略的累计收益率数据。
    """
    return ep.cum_returns(get_strategy_return(strat), starting_value=starting_value)


def check_index_tz(df: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """
    检查索引时区并进行调整。

    参数：
    - df: pd.Series 或 pd.DataFrame
        需要检查时区的数据。

    返回值：
    - Union[pd.Series, pd.DataFrame]
        调整后的具有正确时区的数据。

    示例：
    ```python
    df = pd.DataFrame({'A': [1, 2, 3]}, index=pd.date_range('2022-01-01', periods=3))
    df = check_index_tz(df)
    ```
    """
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    return df
