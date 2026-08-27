function StatsTable({
  match,
  stats
}) {

  const home = stats.find(
    (team) =>
      team.team === match.home_team
  );


  const away = stats.find(
    (team) =>
      team.team === match.away_team
  );


  const rows = [
    [
      "Possession",
      `${home?.possession ?? 0}%`,
      `${away?.possession ?? 0}%`
    ],

    [
      "Shots",
      home?.shots ?? 0,
      away?.shots ?? 0
    ],

    [
      "Shots on Target",
      home?.shots_on_target ?? 0,
      away?.shots_on_target ?? 0
    ],

    [
      "Passes",
      home?.passes ?? 0,
      away?.passes ?? 0
    ],

    [
      "Pass Accuracy",
      `${home?.pass_accuracy ?? 0}%`,
      `${away?.pass_accuracy ?? 0}%`
    ],

    [
      "Corners",
      home?.corners ?? 0,
      away?.corners ?? 0
    ],

    [
      "Fouls",
      home?.fouls ?? 0,
      away?.fouls ?? 0
    ],

    [
      "Yellow Cards",
      home?.yellow_cards ?? 0,
      away?.yellow_cards ?? 0
    ],

    [
      "xG",
      Number(home?.xg ?? 0).toFixed(2),
      Number(away?.xg ?? 0).toFixed(2)
    ],
  ];


  return (
    <section className="analytics-section">

      <div className="section-heading">

        <div>
          <span className="section-label">
            PERFORMANCE
          </span>

          <h2>
            Match Statistics
          </h2>
        </div>

      </div>


      <div className="stats-table">

        <div className="stat-row stat-header">

          <span>
            {match.home_team}
          </span>

          <span>
            Statistic
          </span>

          <span>
            {match.away_team}
          </span>

        </div>


        {rows.map(
          ([label, homeValue, awayValue]) => (

            <div
              className="stat-row"
              key={label}
            >

              <strong>
                {homeValue}
              </strong>

              <span>
                {label}
              </span>

              <strong>
                {awayValue}
              </strong>

            </div>

          )
        )}

      </div>

    </section>
  );
}


export default StatsTable;