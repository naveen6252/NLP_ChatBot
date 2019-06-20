## intent:fact.table.logic
- [month to date](logic:MTD) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise [for](date_condition:equal_to) last month
- [mtd](logic:MTD) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018
- [month to date](logic:MTD) [sales](fact:SalesAmount) for each [employee](dim:Name)
- [mtd](logic:MTD) [sales quantity](fact:SalesQty) for each [employee](dim:Name) [for](date_condition:equal_to) last month
- [m-t-d](logic:MTD) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) this year
- [month to date](logic:MTD) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion)


- [qtd](logic:QTD) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise [for](date_condition:equal_to) last month
- [quarter to date](logic:QTD) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [for](date_condition:equal_to) this year
- [quarter to date](logic:QTD) [sales](fact:SalesAmount) for each [employee](dim:Name) [between](date_condition:greater_than) 2015 [and](date_condition:lesser_than) 2018
- [qtd](logic:QTD) [sales quantity](fact:SalesQty) for each [employee](dim:Name) [for](date_condition:equal_to) last month
- [quarter to date](logic:QTD) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion)
- [q-t-d](logic:QTD) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion)


- [year to date](logic:YTD) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise
- [ytd](logic:YTD) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018
- [year to date](logic:YTD) [sales](fact:SalesAmount) for each [employee](dim:Name) [for](date_condition:equal_to) last year
- [year to date](logic:YTD) [sales quantity](fact:SalesQty) for each [employee](dim:Name)
- [ytd](logic:YTD) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) last month
- [y-t-d](logic:YTD) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) this year


- [month over month](logic:MOM) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise
- [mom](logic:MOM) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [for](date_condition:equal_to) last month
- [month over month](logic:MOM) [sales](fact:SalesAmount) for each [employee](dim:Name)
- [m-o-m](logic:MOM) [sales quantity](fact:SalesQty) for each [employee](dim:Name) [for](date_condition:equal_to) this year
- [mom](logic:MOM) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion)
- [m-o-m](logic:MOM) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) last month


- [quarter over quarter](logic:QOQ) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise [for](date_condition:equal_to) last year
- [qoq](logic:QOQ) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [for](date_condition:equal_to) this year
- [quarter over quarter](logic:QOQ) [sales](fact:SalesAmount) for each [employee](dim:Name)
- [qoq](logic:QOQ) [sales quantity](fact:SalesQty) for each [employee](dim:Name)
- [quarter over quarter](logic:QOQ) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) last month
- [q-o-q](logic:QOQ) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion) 


- [year over year](logic:YOY) [sales](fact:SalesAmount) [customer](dim:CustomerName) wise
- [yoy](logic:YOY) [sales quantity](fact:SalesQty) [customer](dim:CustomerName) wise [for](date_condition:equal_to) last month
- [year over year](logic:YOY) [sales](fact:SalesAmount) for each [employee](dim:Name)
- [y-o-y](logic:YOY) [sales quantity](fact:SalesQty) for each [employee](dim:Name) [for](date_condition:equal_to) last month
- [year over year](logic:YOY) [sales](fact:SalesAmount) in each [region](dim:CustomerRegion) [for](date_condition:equal_to) this year
- [yoy](logic:YOY) [sales quantity](fact:SalesQty) in each [region](dim:CustomerRegion) [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018

- [target achieved](logic:Target-Achievement) by each [customer](dim:CustomerName) [for](date_condition:equal_to) last month
- [target achieved](logic:Target-Achievement) by each [employee](dim:Name)
- [target achieved](logic:Target-Achievement) by all [customers](dim:CustomerName) [for](date_condition:equal_to) last to last month
- [target achieved](logic:Target-Achievement) by all [employees](dim:Name) [for](date_condition:equal_to) last year
- [target achieved](logic:Target-Achievement) by all [customers](dim:CustomerName) in [north](CustomerRegion:North) region [for](date_condition:equal_to) this year

- [mtd](logic:MTD) [sales](fact:SalesAmount) 
- [month to date](logic:MTD) [sales quantity](fact:SalesQty)  
- [m-t-d](logic:MTD) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50) [for](date_condition:equal_to) this year
- [month to date](logic:MTD) [sales quantity](fact:SalesQty) for [customer 50](CustomerName:Customer50)
- [mtd](logic:MTD) [sales](fact:SalesAmount) for [north](CustomerRegion:North) region

- [qtd](logic:QTD) [sales](fact:SalesAmount)
- [quarter to date](logic:QTD) [sales](fact:SalesAmount) [for](date_condition:equal_to) this year
- [qtd](logic:QTD) [sales quantity](fact:SalesQty)  [from](date_condition:greater_than) 2017 [to](date_condition:lesser_than) 2019
- [quarter to date](logic:QTD) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50)
- [q-t-d](logic:QTD) [sales quantity](fact:SalesQty) for [customer 50](CustomerName:Customer50) 


- [ytd](logic:YTD) [sales](fact:SalesAmount)
- [year to date](logic:YTD) [sales](fact:SalesAmount) 
- [year to date](logic:YTD) [sales](fact:SalesAmount) [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018
- [ytd](logic:YTD) [sales quantity](fact:SalesQty)  [for](date_condition:equal_to) this year
- [year to date](logic:YTD) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50)
- [ytd](logic:YTD) [sales quantity](fact:SalesQty) for [customer 50](CustomerName:Customer50)


- [mom](logic:MOM) [sales](fact:SalesAmount)
- [month over month](logic:MOM) [sales quantity](fact:SalesQty)  
- [month over month](logic:MOM) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50) [for](date_condition:equal_to) this year
- [mom](logic:MOM) [sales quantity](fact:SalesQty) for [customer 50](CustomerName:Customer50) 


- [quarter over quarter](logic:QOQ) [sales](fact:SalesAmount)
- [qoq](logic:QOQ) [sales quantity](fact:SalesQty)  
- [q-o-q](logic:QOQ) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50) [from](date_condition:greater_than) 2015 [to](date_condition:lesser_than) 2018
- [quarter over quarter](logic:QOQ) [sales quantity](fact:SalesQty) for [customer 50](CustomerName:Customer50) [for](date_condition:equal_to) last month


- [year over year](logic:YOY) [sales](fact:SalesAmount)
- [yoy](logic:YOY) [sales quantity](fact:SalesQty)  
- [year over year](logic:YOY) [sales](fact:SalesAmount) for [customer 50](CustomerName:Customer50) [for](date_condition:equal_to) this year


- [target achieved](logic:Target-Achievement) by [customer 50](CustomerName:Customer50) [for](date_condition:equal_to) previous month
- [target achieved](logic:Target-Achievement) by [emp50](Name:Emp050) [for](date_condition:equal_to) last month
- [target achieved](logic:Target-Achievement) by [emp50](Name:Emp050) in [Govt](CustomerType:Govt) [for](date_condition:equal_to) last year
- [mtd](logic:MTD)
- [qtd](logic:QTD)
- [ytd](logic:YTD)