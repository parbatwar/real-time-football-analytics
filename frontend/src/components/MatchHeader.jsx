function MatchHeader({
  match,
  events,
  live = false
}) {

  const homeGoals = events.filter(
    (event) =>
      event.event_type === "GOAL" &&
      event.team === match.home_team
  ).length;


  const awayGoals = events.filter(
    (event) =>
      event.event_type === "GOAL" &&
      event.team === match.away_team
  ).length;


  return (
    <section className="match-card">

      <div className="match-card-top">

        <div>
          <span className="competition">
            {match.competition}
          </span>

          <span className="match-id">
            {match.match_id}
          </span>
        </div>


        {live && (
          <div className="live-badge">
            <span className="live-dot"></span>
            LIVE
          </div>
        )}

      </div>


      <div className="match-score">

        <div className="score-team">

          <span className="team-type">
            HOME
          </span>

          <h2>
            {match.home_team}
          </h2>

          <strong>
            {homeGoals}
          </strong>

        </div>


        <div className="match-center">

          <span className="match-status">
            {match.status}
          </span>

          <strong>
            {match.current_minute}'
          </strong>

          <span className="vs">
            VS
          </span>

        </div>


        <div className="score-team">

          <span className="team-type">
            AWAY
          </span>

          <h2>
            {match.away_team}
          </h2>

          <strong>
            {awayGoals}
          </strong>

        </div>

      </div>

    </section>
  );
}


export default MatchHeader;