import { config } from "../../Constants";

const makeQuery = (ids, period, pollutants) => {
  let qParams = ids.reduce((prev, id) => prev + `ids=${id}&`, "?");
  let timeParam = `period=${period.query()}`;
  const truePollutants = Object.entries(pollutants).reduce(
    (prev, [key, value]) => {
      if (value) {
        prev.push(key);
      }
      return prev;
    },
    []
  );

  const pollutantsParam =
    truePollutants.length === 0
      ? ""
      : `&pollutants=${truePollutants.join("&pollutants=")}`;

  qParams = qParams + timeParam + pollutantsParam;
  return qParams;
};

const getReadings = async (ids, period) => {
  let params = makeQuery(ids, period);
  const response = await fetch(`${config.urls.READINGS_URL}${params}`);
  const data = await response.json();

  return data;
};

export default getReadings