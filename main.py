import datetime

# Phase 1
def ValidSymbol(symbol):
  parts = symbol.strip().split("-")
  return (len(parts) == 2 and parts[1] == "USDT")
 
def ParseInput(input):
  parts = input.strip().split()

  if len(parts) != 4:
    print("Invalid input")
    return -1
  
  action, symbol, amount, price = parts

  if action != "BUY" and action != "SELL":
    print("Invalid ACTION")
    return -1
  if not ValidSymbol(symbol):
    print("Invalid SYMBOL")
    return -1
  if float(amount) <= 0 or float(price) <= 0:
    print("Invalid AMOUNT/PRICE")
    return -1

  return parts

def Fees(amount, price):
  total = amount * price
  if total <= 10000000:
    fee = 0.005 * total
  else:
    fee = 0.002 * total

  return [fee, total - fee]

def UUID(symbol):
  time = datetime.datetime.now()
  seed = 0
  for c in symbol:
    seed += ord(c)
  seed = abs(seed) % 100
  uuid = f"{time.strftime('%H%M%S')}{symbol}{str(seed).zfill(2)}"
  return uuid

# Phase 2
def UpdateMarket(market):
  multi = 0.98 if (int(datetime.datetime.now().strftime("%S")) % 2 == 0) else 1.05
  new_market = []
  for (symbol, price, history) in market:
    new_price = multi * price
    history.insert(0, new_price)
    new_history = list(history)
    new_market.append((symbol, new_price, new_history))
  return new_market

def PrintMarket(market):
  for (symbol, price, history) in market:
    if len(history) < 3:
      continue
    avg = (history[0] + history[1] + history[2]) / 3
    print(f"{symbol}: Current Price = {price}, Average Price = {avg}")

# Phase 3
def Buy(symbol, amount, market, wallet):
  cur_price = -1
  for (symboll, price, history) in market:
    if symboll == symbol:
      cur_price = price
      break
  money = -1
  for cur, value in wallet:
    if cur == "USDT":
      money = value
      break

  if cur_price == -1:
    print("Invalid currency")
    return -1
  if money == -1:
    print("Invalid symbol")
    return -1
  if money < cur_price*amount:
    print("Not enough money in wallet")
    return 0
  
  found = False
  for i in range(len(wallet)):
    if wallet[i][0] == "USDT":
      wallet.pop(i)
      found = True
      break
  if not found:
    print("Internal Error")
    return -1

  new = ()
  for i in range(len(wallet)):
    if f"{wallet[i][0]}-USDT" == symbol:
      new = (wallet[i][0],  wallet[i][1] + amount)
      wallet.pop(i)
      break
  if len(new) == 0:
    print("Internal Error")
    return -1

  wallet.append(("USDT", money - (cur_price * amount)))
  wallet.append(new)

# Phase 4
def FindPrice(cur, market):
  if cur == "USDT":
    return 1
  for symbol, price, history in market:
    if f"{cur}-USDT" == symbol:
      return price
  return 0

def Sum(market, wallet):
  sum = 0
  values = list(map(lambda v : FindPrice(v[0], market)*v[1], wallet))
  for x in values:
    sum += x
  return [values, sum]

def MyFilter(record):
  symbol, price, history = record
  avg = 0
  for x in history:
    avg += x
  avg /= len(history)
  delta = (avg - price) / avg
  return (delta > 0.1)

def Forsat(market):
  return list(filter(MyFilter, market))

def Zip(old, new):
  diff = list(map(lambda i: (new[i] - old[i])/old[i], range(len(old))))
  return list(zip(old, new, diff))

def Report(market, wallet, **kwargs):
  for cur, amount in wallet:
    if kwargs["exclude_zeros"] and amount == 0:
      continue
    print(f"{cur} --> {amount}")

def PrintSep():
  print("------------------------------------------------")
  
def main():
  Market = [
      ("BTC-USDT", 60000, [59000, 61000, 50000]),
      ("GBP-USDT", 1.34, [1.35, 1.39, 1.30]),
      ("CNY-USDT", 0.14, [0.142, 0.145, 0.148]),
      ("EUR-USDT", 1.09, [1.0812, 1.0847, 1.0889]),
      ("GBP-USDT", 1.01, [1.2615, 1.2650, 1.2698]),
      ("AUD-USDT", 0.66, [0.6541, 0.6568, 0.6599]),
  ]

  Wallet = [("USDT", 1000000000), ("BTC", 0.5), ("GBP", 50), ("EUR", 0), ("CNY", 0)]
  
  while True:
    Market = UpdateMarket(Market)
    PrintMarket(Market)
    print(Wallet)
    PrintSep()

    s = input("> ")
    if len(s) == 0:
      # break
      print(Sum(Market, Wallet))
      print(Forsat(Market))
      print(Zip([1.5, 1.49, 1.51], [1.48, 1.61, 1.40]))
      Report(Market, Wallet, exclude_zeros = True)
      PrintSep()
      continue

    parts = ParseInput(s)
    if parts == -1:
      continue
    action, symbol, amount, price = parts
    amount = float(amount)
    price = float(price)

    print(Fees(amount, price))
    print(UUID(symbol))

    if action == "BUY":
      Buy(symbol, amount, Market, Wallet)

    PrintSep()


if __name__ == "__main__":
  main()
