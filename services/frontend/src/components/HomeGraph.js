import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const HomeGraph = (props) => {
  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "aqi data",
      },
    },
  };
  const aqiData = props.aqiData;
  const labels = props.dates;
  const data = {
    labels,
    datasets: aqiData.map((station) => {
      const randm = Math.floor(Math.random() * 220 + 30);
      return {
        label: station["station_id"],
        data: station["data"],
        borderColor: `rgb(255, ${randm - 30}, ${randm}`,
        backgroundColor: `rgb(255, 99, ${randm}, 0.5)`,
      };
    }),
  };

  return (
    <div className="graph-container">
      <Line options={options} data={data} />
    </div>
  );
};

export default HomeGraph;
