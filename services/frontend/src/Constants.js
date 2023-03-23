const prod = {
  urls: {
    STATIONS_URL: "https://airboo.ak0.io/api/stations/all-nearby/?zipcode=",
    READINGS_URL: "https://airboo.ak0.io/api/air-readings/from-ids/",
  },
};

const dev = {
  urls: {
    STATIONS_URL: "http://localhost:10100/api/stations/all-nearby/?zipcode=",
    READINGS_URL: "http://localhost:10100/api/air-readings/from-ids/",
  },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
