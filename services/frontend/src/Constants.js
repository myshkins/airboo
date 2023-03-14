const prod = {
  urls: {
    STATIONS_URL: "http://localhost:8100/stations/all-nearby/?zipcode=",
    READINGS_URL: "http://localhost:8100/air-readings/from-ids/",
  },
};

const dev = {
  urls: {
    STATIONS_URL: "http://localhost:8100/stations/all-nearby/?zipcode=",
    READINGS_URL: "http://localhost:8100/air-readings/from-ids/",
  },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
