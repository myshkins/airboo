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

// const labels = ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'];
// export const data = {
//   labels,
//   datasets: [
//     {
//       label: "Dataset 1",
//       data: labels.map(() => Math.random() * 10),
//       borderColor: "rgb(255, 99, 132)",
//       backgroundColor: "rgba(255, 99, 132, 0.5)",
//     },
//     {
//       label: "Dataset 2",
//       data: labels.map(() => Math.random() * 10),
//       borderColor: "rgb(53, 162, 235)",
//       backgroundColor: "rgba(53, 162, 235, 0.5)",
//     },
//   ],
// };

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
