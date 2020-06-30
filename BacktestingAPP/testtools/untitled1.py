
import virtuese as vs
import pickyinvestor
import datamonger

dp = datamonger.Datamonger()
df2 = dp.getHuShen300IndexComponent()


# 初始化一个对象实例
backtrader = vs.VirtueSE()

# 必须设置回测日期
backtrader.setRunningInterval('20190601', '20200601')

# 必须设置价格回测方式
backtrader.setBacktestingPriceEngine("backward")

# 可选设置一个股票池
#backtrader.setStockPool(df2['con_code'].tolist())

# 可选创建本次回测的临时数据库
backtrader.createMarketExpressDB("testMarket.db", "20200613DTestME.db")


# 加载两个数据库
backtrader.setBrokerDB("aTest.db")#交易记录 历史记录 是输出文件 每次运行现在需要删掉
backtrader.setMarketExpressDB("20200613DTestME.db")

# 初始化策略实例
strategy = pickyinvestor.PickyInvestor()

# 加载策略
backtrader.setTradingStrategy(strategy)

backtrader.execute()

testoutput = backtrader.testoutput
print(testoutput)
