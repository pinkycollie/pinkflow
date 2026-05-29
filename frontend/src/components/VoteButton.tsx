import { useState } from "react";

export default function VoteButton() {
  const [votes, setVotes] = useState(0);

  const vote = async () => {
    const res = await fetch("/api/vote", { method: "POST" });
    if (res.ok) {
      setVotes(votes + 1);
    }
  };

  return (
    <button onClick={vote} className="vote-button">
      Vote! ({votes})
    </button>
  );
}