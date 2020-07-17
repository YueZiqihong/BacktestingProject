# Backend APP to support backtesting
This app handles HTML requests and will send parameters for the backtesting system and/or interact with the database. Data are stored in reportdb.db.  
Also removes temporary files created by the testtools package.
## /testtools
This package is created by Yiming Zhang.
Contains logic when executing strategies if all parameters are given. Since the package was initially intended for his personal use, it is not recommend to use without context.
