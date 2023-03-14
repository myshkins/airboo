class Pollutant {
  static pollutants = {
    pm25: false,
    pm10: false,
    o3: false,
    co: false,
    no2: false,
    so2: false,
  }

  constructor(...args) {
    this.table = this.pollutants
    args.forEach((arg) => {
      this.table[arg] = true
    })
    Object.freeze(this)
  }
}

export default Pollutant