const prod = {
  urls: {
    STATIONS_URL: "https://airboo.ak0.io/api/stations/all-nearby/?zipcode=",
    READINGS_URL: "https://airboo.ak0.io/api/air-readings/from-ids/",
    POLLUTANTS_URL: "https://airboo.ak0.io/api/air-readings/pollutants/"
  },
};

const dev = {
  urls: {
    STATIONS_URL: "http://localhost:10100/api/stations/all-nearby/?zipcode=",
    READINGS_URL: "http://localhost:10100/api/air-readings/from-ids/",
    POLLUTANTS_URL: "http://localhost:10100/api/air-readings/pollutants/"
  },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
