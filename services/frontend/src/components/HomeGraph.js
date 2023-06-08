import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Colors,
} from "chart.js";
import { Line } from "react-chartjs-2";

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Colors,
);

Chart.defaults.color = '#A5A1AC'
// Chart.defaults.elements.line.cubicInterpolationMode = 'default'
const HomeGraph = (props) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      colors: {
        forceOverride: true
      },
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "aqi data",
      },
    },
    scales: {
      y: {
        min: 0,
        max: 250
      }
    }
  };
  const aqiData = props.aqiData;
  const labels = props.dates;
  const data = {
    labels,
    datasets: aqiData.map((pollut) => {
      return {
        label: pollut["datasetName"],
        data: pollut["data"],
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
