# -*- coding: utf-8 -*-
"""app_conv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14Pwb9yG1ihX8oWkF1pCN3Zlvlse1wSbh
"""

import streamlit as st
import requests
import json
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# کلاس برای نمایش اطلاعات یک سهم
class Stock:
  def __init__(self, symbol, name, price, change, volume):
    self.symbol = symbol
    self.name = name
    self.price = price
    self.change = change
    self.volume = volume

  def __str__(self):
    return f"{self.symbol} ({self.name}): {self.price} ({self.change})"

# تابع برای دریافت اطلاعات سهام
def get_stocks():
  # دریافت اطلاعات سهام از یاهو فایننس
  urls = [
    "https://finance.yahoo.com/quote/GLD/history?p=GLD",
    "https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD",
    "https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD",
    "https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD"
  ]
  responses = [requests.get(url) for url in urls]
  datas = [json.loads(response.text) for response in responses]

  # لیست قیمت‌های سهام
  stocks = []
  for data in datas:
    stocks.append(Stock(data["symbol"], data["name"], data["regularMarketPrice"], data["regularMarketChange"], data["regularMarketVolume"]))

  return stocks

# تابع برای دریافت اخبار روزانه
def get_news():
  # دریافت اخبار روزانه از یاهو فایننس
  url = "https://finance.yahoo.com/news/"
  response = requests.get(url)
  data = json.loads(response.text)

  # لیست اخبار
  news = []
  for item in data["articles"]:
    news.append({
      "title": item["title"],
      "url": item["url"],
      "source": item["source"],
      "publishedAt": item["publishedAt"]
    })

  return news

# تابع برای خرید و فروش سهام
def buy_stock(stock, price):
  # خرید سهام
  print(f"خرید {stock.symbol} به قیمت {price}")

# تابع برای فروش سهام
def sell_stock(stock, price):
  # فروش سهام
  print(f"فروش {stock.symbol} به قیمت {price}")

# تابع برای پیش‌بینی قیمت سهام با استفاده از الگوریتم دیپ کانولوشنال
def predict_price(stock, days):
  # دریافت قیمت‌های گذشته
  prices = stock.history(periods=days)

  # ساخت مدل دیپ کانولوشنال
  model = Sequential()
  model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(prices.shape[1],)))
  model.add(MaxPooling2D((2, 2)))
  model.add(Flatten())
  model.add(Dense(1, activation="relu"))
  model.compile(optimizer="adam", loss="mse")

  # آموزش مدل
  model.fit(prices.values, prices.values[:, 0], epochs=10)

  # پیش‌بینی قیمت‌های آینده
  predictions = model.predict(prices.values)[:, 0]

  # بازگشت پیش‌بینی‌ها
  return predictions

# تابع اصلی
def main():
  # نمایش عنوان
  st.title("بازار سهام")

  # دریافت اطلاعات سهام
  stocks = get_stocks()
  # نمایش اطلاعات سهام
  for stock in stocks:
    st.write(f"**{stock.symbol}** ({stock.name})")
    st.write(f"قیمت فعلی: {stock.price}")
    st.write(f"درصد تغییر: {stock.change}")
    st.write(f"حجم معاملات: {stock.volume}")
    st.write("**اخبار روزانه:**")
    for news in get_news():
      st.write(f"* {news['title']} (از منبع {news['source']})")
