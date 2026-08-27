import {
  useEffect,
  useState
} from "react";

import {
  Link
} from "react-router-dom";


const API = "http://localhost:8000";


function HistoryPage() {

  const [matches, setMatches] =
    useState([]);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    const fetchMatches = async () => {

      try {

        const response = await fetch(
          `${API}/matches`,
          {
            cache: "no-store"
          }
        );

        const data =
          await response.json();


        const sorted = [
          ...data
        ].sort(
          (a, b) => {

            const aNumber = parseInt(
              a.match_id.replace(
                "match_",
                ""
              )
            );

            const bNumber = parseInt(
              b.match_id.replace(
                "match_",
                ""
              )
            );

            return bNumber - aNumber;

          }
        );


        // Latest match stays on homepage.
        // Everything older is history.

        setMatches(
          sorted.slice(2)
        );

        setLoading(false);


      } catch (error) {

        console.error(
          "HISTORY ERROR:",
          error
        );

        setLoading(false);

      }

    };


    fetchMatches();

  }, []);


  if (loading) {

    return (
      <div className="page-message">
        Loading match history...
      </div>
    );

  }


  return (
    <main className="page-container">

      <div className="page-heading">

        <div>

          <span className="section-label" style={{ textAlign: "left" }}>
            ARCHIVE
          </span>

          <h1 style={{ textAlign: "left" }}>
            Match History
          </h1>

          <p style={{ textAlign: "left" }}>
            Previously recorded football matches.
          </p>

        </div>

      </div>


      {!matches.length ? (

        <div className="empty-state">

          No previous matches available.

        </div>

      ) : (

        <div className="history-grid">

          {matches.map(
            (match) => (

              <Link

                to={`/history/${match.match_id}`}

                className="history-card"

                key={match.match_id}

              >

                <div className="history-top">

                  <span>
                    {match.match_id}
                  </span>

                  <span className="history-status">
                    {match.current_minute >= 90
                      ? "FULL TIME"
                      : match.status}
                  </span>

                </div>


                <div className="history-teams">

                  <strong>
                    {match.home_team}
                  </strong>

                  <span>
                    vs
                  </span>

                  <strong>
                    {match.away_team}
                  </strong>

                </div>


                <div className="history-footer">

                  <span>
                    {match.competition}
                  </span>

                  <span>
                    View analytics →
                  </span>

                </div>

              </Link>

            )
          )}

        </div>

      )}

    </main>
  );
}


export default HistoryPage;