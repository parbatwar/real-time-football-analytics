import {
  useEffect,
  useState
} from "react";

import {
  Link,
  useParams
} from "react-router-dom";

import MatchHeader from "../components/MatchHeader";
import StatsTable from "../components/StatsTable";
import Timeline from "../components/Timeline";


const API = "http://localhost:8000";


function MatchDetailsPage() {

  const { matchId } = useParams();


  const [match, setMatch] =
    useState(null);

  const [stats, setStats] =
    useState([]);

  const [events, setEvents] =
    useState([]);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    const fetchData = async () => {

      try {

        const [
          matchResponse,
          statsResponse,
          eventsResponse
        ] = await Promise.all([

          fetch(
            `${API}/matches/${matchId}`
          ),

          fetch(
            `${API}/matches/${matchId}/team-stats`
          ),

          fetch(
            `${API}/matches/${matchId}/events`
          )

        ]);


        setMatch(
          await matchResponse.json()
        );

        setStats(
          await statsResponse.json()
        );

        setEvents(
          await eventsResponse.json()
        );

        setLoading(false);


      } catch (error) {

        console.error(
          "MATCH DETAILS ERROR:",
          error
        );

        setLoading(false);

      }

    };


    fetchData();

  }, [matchId]);


  if (loading) {

    return (
      <div className="page-message">
        Loading match...
      </div>
    );

  }


  if (!match) {

    return (
      <div className="page-message">
        Match not found.
      </div>
    );

  }


  return (
    <main className="page-container">

      <Link
        to="/history"
        className="back-link"
      >
        ← Match History
      </Link>


      <div className="page-heading">

        <div>

          <span className="section-label" style={{ textAlign: "left" }}>
            MATCH REPORT
          </span>

          <h1 style={{ textAlign: "left" }}>
            {match.home_team}
            {" vs "}
            {match.away_team}
          </h1>

        </div>

      </div>


      <MatchHeader
        match={match}
        events={events}
      />


      <div className="analytics-grid">

        <StatsTable
          match={match}
          stats={stats}
        />

        <Timeline
          events={events}
          limit={1000}
        />

      </div>

    </main>
  );
}


export default MatchDetailsPage;