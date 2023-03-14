class TimePeriod {
  static twelveHR = new TimePeriod("12hr")
  static twentyFourHR = new TimePeriod("24hr")
  static fortyEightHR = new TimePeriod("48hr") 
  static fiveDay = new TimePeriod("5day") 
  static tenDay = new TimePeriod("10day") 
  static oneMonth = new TimePeriod("1mon") 
  static oneYear = new TimePeriod("1yr") 
  static allTime = new TimePeriod("all time") 

  constructor(key) {
    this.key = key
    this.table = {
      "12hr": "twelve_hr",
      "24hr": "twenty_four_hr",
      "48hr": "forty_eight_hr",
      "5day": "five_day",
      "10day": "ten_day",
      "1mon": "one_month",
      "1yr": "one_year",
      "all_time": "all_time",
    }
    Object.freeze(this)
  }

  query() {
   return this.table[this.key] 
  }
}

export default TimePeriod