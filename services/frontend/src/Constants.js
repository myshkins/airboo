const prod = {
  urls: {
      STATIONS_URL: '',
      READINGS_URL: '',
  }
}

const dev = {
  urls: {
    STATIONS_URL: 'http://localhost:8100/stations/all-nearby/?zipcode=',
    READINGS_URL: ''
  }
}

export const config = process.env.NODE_ENV === 'development' ? dev: prod