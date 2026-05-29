import { Bar } from "react-chartjs-2";

export default function RepoContributorsChart({ data }) {
  const chartData = {
    labels: data.map(contributor => contributor.name),
    datasets: [
      {
        label: "Contributions",
        data: data.map(contributor => contributor.contributions),
        backgroundColor: "rgba(75, 192, 192, 0.2)"
      }
    ]
  };

  return <Bar data={chartData} />;
}